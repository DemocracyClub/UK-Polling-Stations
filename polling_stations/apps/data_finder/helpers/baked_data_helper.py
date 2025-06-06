import abc
import logging
from pathlib import Path
from typing import Optional
from urllib.parse import urljoin, urlparse

import polars
from django.conf import settings
from requests import Session
from requests.adapters import HTTPAdapter
from requests.exceptions import HTTPError, RequestException
from uk_geo_utils.helpers import Postcode
from urllib3.util.retry import Retry
from sentry_sdk import set_context, get_current_scope


logger = logging.getLogger(__name__)
session = Session()

retries = Retry(
    total=1,
    connect=1,
    backoff_factor=0.1,
    status_forcelist=[502, 503, 504],
    allowed_methods={"GET"},
)

session.mount(
    f"{urlparse(settings.EE_BASE).scheme}://", HTTPAdapter(max_retries=retries)
)


def ballot_paper_id_to_ee_url(ballot_paper_id):
    path = f"/api/elections/{ballot_paper_id}/"
    return urljoin(settings.EE_BASE, path)


class BaseBakedElectionsHelper(abc.ABC):
    def __init__(self, **kwargs): ...

    @abc.abstractmethod
    def get_response(self, postcode: Postcode, uprn: Optional[str] = None):
        raise NotImplementedError


class NoOpElectionsHelper(BaseBakedElectionsHelper):
    """
    Just returns nothing, causing the app to use EE as it previously did.

    This maintains the previous default behaviour for looking up elections

    """

    def get_response(self, postcode: Postcode, uprn: Optional[str] = None):
        return {}


class LocalParquetElectionsHelper(BaseBakedElectionsHelper):
    def __init__(self, elections_parquet_path: Path = None, **kwargs):
        self.elections_parquet_path = elections_parquet_path or getattr(
            settings, "ELECTION_PARQUET_DATA_PATH", None
        )
        if not self.elections_parquet_path:
            raise ValueError(
                "Path to local parquet files required for local parquet backend"
            )
        super().__init__(**kwargs)

    def get_response(self, postcode: Postcode, uprn: Optional[str] = None):
        result = self.get_ballot_list(postcode, uprn)

        if not result["address_picker"]:
            try:
                result["ballots"] = self.get_full_ballots(result["ballot_ids"])
            except HTTPError as e:
                message = f"Error fetching {e.request.url}: {e.response.status_code}"
                # attach details about the response to the sentry event as context
                set_context(
                    "http_response",
                    {
                        "status_code": e.response.status_code,
                        "headers": dict(e.response.headers),
                        "truncated_body": e.response.text[:1000],
                    },
                )
                scope = get_current_scope()
                scope.fingerprint = ["error_fetching_url", str(e.response.status_code)]
                logging.error(message)

                result["ballots"] = []
                result["request_success"] = False
            except RequestException as e:
                message = f"Exception fetching {e.request.url}: {e.__class__}"
                scope = get_current_scope()
                scope.fingerprint = ["exception_fetching_url"]
                logging.error(message)

                result["ballots"] = []
                result["request_success"] = False

        return result

    def get_full_ballots(self, ballot_ids):
        result = []
        for ballot_id in ballot_ids:
            url = ballot_paper_id_to_ee_url(ballot_id)
            response = session.get(url, timeout=5)
            response.raise_for_status()
            result.append(response.json())
        return result

    def get_file_path(self, postcode: Postcode):
        outcode = postcode.with_space.split()[0]
        return self.elections_parquet_path / f"{outcode}.parquet"

    def get_ballot_list(self, postcode: Postcode, uprn: Optional[str] = None):
        parquet_filepath = self.get_file_path(postcode)
        try:
            df = polars.read_parquet(parquet_filepath)
        except FileNotFoundError:
            # ERROR
            # In theory this shouldn't happen
            # every outcode should exists as a parquet file
            message = f"Expected file {parquet_filepath} not found"
            scope = get_current_scope()
            scope.fingerprint = ["parquet:expected_parquet_file_not_found"]
            logging.error(message)
            return {"address_picker": False, "ballot_ids": [], "request_success": False}

        if df.height == 0:
            # VALID
            # If the file is empty it should mean that there are no current
            # elections for this outcode. Just return an empty ballots list.
            return {"address_picker": False, "ballot_ids": [], "request_success": True}

        if "ballot_ids" in df.columns:
            # TODO Remove this if we change the name at source
            df = df.rename({"ballot_ids": "current_elections"})

        # TODO: This isn't needed if the Parquet casts the list to a string
        #       at the point of creation
        df = df.with_columns(
            polars.col("current_elections")
            .cast(polars.List(polars.Utf8))
            .list.join(",")
        )

        df = df.filter((polars.col("postcode") == postcode.with_space))
        if df.is_empty():
            # ERROR
            # In theory this shouldn't happen. If the postcode exists in AddressBase
            # and the outcode file is non-empty, we should get results.
            message = f"Expected postcode {postcode.with_space} not found in file {parquet_filepath}"
            scope = get_current_scope()
            scope.fingerprint = ["parquet:expected_postcode_not_found_not_found"]
            logging.error(message)
            return {"address_picker": False, "ballot_ids": [], "request_success": False}

        if uprn:
            df = df.filter((polars.col("uprn") == uprn))
            if df.height == 0:
                # ERROR
                # In theory this shouldn't happen
                # but if our 2 copies of AddressBase (local DB and parquet files)
                # are out of sync this will totally happen at some point
                message = (
                    f"UPRN {uprn} did not exist in Parquet file {parquet_filepath}"
                )
                scope = get_current_scope()
                scope.fingerprint = ["parquet:uprn_not_in_parquet_file"]
                logging.error(message)
                return {
                    "address_picker": False,
                    "ballot_ids": [],
                    "request_success": False,
                }
            if df.height > 1:
                # ERROR
                # Again, this this shouldn't happen in theory
                # A UPRN should only appear in our data once or zero times
                # Those are the valid options
                message = f"UPRN {uprn} found {df.height} times in Parquet file {parquet_filepath}"
                scope = get_current_scope()
                scope.fingerprint = ["parquet:duplicate_urpn"]
                logging.error(message)
                return {
                    "address_picker": False,
                    "ballot_ids": [],
                    "request_success": False,
                }

            # VALID
            return {
                "address_picker": False,
                "ballot_ids": []
                if df["current_elections"][0] == ""
                else df["current_elections"][0].split(","),
                "request_success": True,
            }

        # Count the unique values in the `ballot_ids` column.
        # If there is more than one value, count the postcode as split
        is_split = (
            df.select(polars.col("current_elections").n_unique()).to_series()[0] > 1
        )

        if is_split:
            # VALID
            return {"address_picker": True, "ballot_ids": [], "request_success": True}

        # VALID
        return {
            "address_picker": is_split,
            "ballot_ids": []
            if df["current_elections"][0] == ""
            else df["current_elections"][0].split(","),
            "request_success": True,
        }
