import abc
import asyncio
import logging
from pathlib import Path
from typing import Optional
from urllib.parse import urljoin

import httpx
import polars
from django.conf import settings
from uk_geo_utils.helpers import Postcode
from sentry_sdk import capture_message, set_context

logger = logging.getLogger(__name__)


async def fetch(client, url):
    # fetch from a URL
    # if anything fails, just log an error and return None
    try:
        response = await client.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            message = f"Error fetching {url}: {response.status_code}"
            logging.error(message)
            # attach details about the response to the sentry event as context
            set_context(
                "http_response",
                {
                    "status_code": response.status_code,
                    "headers": dict(response.headers),
                    "truncated_body": response.text[:1000],
                },
            )
            capture_message(message, level="error")
            return None
    except Exception as e:
        message = f"Exception fetching {url}: {e.__class__}"
        logging.error(message)
        capture_message(message, level="error")
        return None


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
            result["ballots"] = self.get_full_ballots(result["ballot_ids"])
            # TODO: how to set request_success if some requests failed here?

        return result

    def get_full_ballots(self, ballot_ids):
        urls = [ballot_paper_id_to_ee_url(ballot_id) for ballot_id in ballot_ids]

        async def fetch_all():
            async with httpx.AsyncClient() as client:
                responses = await asyncio.gather(*(fetch(client, url) for url in urls))
            # filter out any responses that did not return a valid object
            return [resp for resp in responses if resp is not None]

        return asyncio.run(fetch_all())

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
            logger.error(message)
            capture_message(message, level="error")
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
            logger.error(message)
            capture_message(message, level="error")
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
                logger.error(message)
                capture_message(message, level="error")
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
                logger.error(message)
                capture_message(message, level="error")
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
