import abc
from pathlib import Path
from typing import List, Tuple, Optional
from urllib.parse import urljoin

import polars
from data_finder.helpers import EveryElectionWrapper
from data_finder.helpers.every_election import StaticElectionsAPIElectionWrapper
from django.conf import settings
from requests import Session
from uk_geo_utils.helpers import Postcode

session = Session()


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

    ee_wrapper = EveryElectionWrapper

    def get_response(self, postcode: Postcode, uprn: Optional[str] = None):
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

    def get_response(self, postcode: Postcode, uprn: Optional[str] = None):
        is_split, data_for_postcode = self.get_ballot_list(postcode, uprn)
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

    def get_ballot_list(
        self, postcode: Postcode, uprn: Optional[str] = None
    ) -> Tuple[bool, List]:
        try:
            df = polars.read_parquet(self.get_file_path(postcode))
        except FileNotFoundError:
            # If the file isn't found it should mean that there are no current
            # elections for this outcode. Just return an empty ballots list.
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

        if uprn:
            df = df.filter((polars.col("uprn") == uprn))
            if len(df) == 0:
                # In theory this shouldn't happen
                # but if our 2 copies of AddressBase (local DB and parquet files)
                # are out of sync this will totally happen at some point
                raise ValueError("NOPE")
            if len(df) > 1:
                # BUG!
                raise ValueError("WTF?!")
            return False, df["current_elections"][0].split(",")

        # Count the unique values in the `ballot_ids` column.
        # If there is more than one value, count the postcode as split
        is_split = (
            df.select(polars.col("current_elections").n_unique()).to_series()[0] > 1
        )

        if is_split:
            return is_split, []

        return is_split, df["current_elections"][0].split(",")
