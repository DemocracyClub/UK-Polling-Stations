import abc
import enum
from pathlib import Path
from typing import List, Tuple
from urllib.parse import urljoin

import polars
from data_finder.helpers import EveryElectionWrapper
from data_finder.helpers.every_election import StaticElectionsAPIElectionWrapper
from django.conf import settings
from requests import Session
from uk_geo_utils.helpers import Postcode

session = Session()


@enum.unique
class BakedElectionsHelperMode(enum.Enum):
    REMOTE = "REMOTE"
    S3 = "S3"
    LOCAL = "LOCAL"


def ballot_paper_id_to_static_url(ballot_paper_id):
    parts = ballot_paper_id.split(".")
    path = "/".join((parts[-1], parts[0], parts[1], f"{ballot_paper_id}.json"))
    return urljoin(settings.WCIVF_BALLOT_CACHE_URL, path)


def ballot_paper_id_to_ee_url(ballot_paper_id):
    path = f"/api/elections/{ballot_paper_id}/"
    return urljoin(settings.EE_BASE, path)


class BaseBakedElectionsHelper(abc.ABC):
    def __init__(self, **kwargs): ...

    @abc.abstractmethod
    def get_response_for_postcode(self, postcode: Postcode):
        raise NotImplementedError


class NoOpElectionsHelper(BaseBakedElectionsHelper):
    """
    Just returns nothing, causing the app to use EE as it previously did.

    This maintains the previous default behaviour for looking up elections

    """

    ee_wrapper = EveryElectionWrapper

    def get_response_for_postcode(self, postcode: Postcode):
        return {}


class LocalParquetElectionsHelper(BaseBakedElectionsHelper):
    ee_wrapper = StaticElectionsAPIElectionWrapper

    def __init__(self, elections_parquet_path: Path = None, **kwargs):
        self.elections_parquet_path = elections_parquet_path or getattr(
            settings, "ELECTION_PARQUET_DATA_PATH", None
        )
        if not self.elections_parquet_path:
            raise ValueError(
                "Path to local parquet files required for local parquet backend"
            )
        super().__init__(**kwargs)

    def get_response_for_postcode(self, postcode: Postcode):
        is_split, data_for_postcode = self.get_ballot_list(postcode)
        data = {
            "address_picker": is_split,
            "addresses": [],
        }

        if is_split:
            data["addresses"] = data_for_postcode
        else:
            data["ballots"] = self.get_full_ballots(data_for_postcode)

        return data

    def get_full_ballots(self, ballot_ids):
        result = []
        for ballot_id in ballot_ids:
            url = ballot_paper_id_to_ee_url(ballot_id)
            req = session.get(url)
            result.append(req.json())
        return result

    def get_file_path(self, postcode: Postcode):
        outcode = postcode.with_space.split()[0]
        return self.elections_parquet_path / f"{outcode}.parquet"

    def get_ballot_list(self, postcode: Postcode) -> Tuple[bool, List]:
        try:
            df = polars.read_parquet(self.get_file_path(postcode))
        except FileNotFoundError:
            # If the file isn't found it should mean that there are no current
            # elections for this outcode. Just return an empty dates list.
            return False, []

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
            # This file doesn't have any rows matching the given postcode
            # Just return an empty list as this means there aren't elections here.
            return False, []

        # Count the unique values in the `ballot_ids` column.
        # If there is more than one value, count the postcode as split
        is_split = (
            df.select(polars.col("current_elections").n_unique()).to_series()[0] > 1
        )

        if is_split:
            return is_split, []

        return is_split, df["current_elections"][0].split(",")


class RemoteBakedElectionsHelper(BaseBakedElectionsHelper):
    def __init__(self, api_key=None, **kwargs):
        self.api_key = api_key or getattr(settings, "DEVS_DC_API_KEY", None)
        if not self.api_key:
            raise ValueError("API key required for remote backend")
        super().__init__(**kwargs)

    def get_response_for_postcode(self, postcode: Postcode):
        req = session.get(
            urljoin(
                settings.DEVS_DC_BASE,
                f"/api/v1/elections/postcode/{postcode.with_space}/",
            ),
            params={"auth_token": self.api_key},
        )
        req.raise_for_status()
        return req.json()
