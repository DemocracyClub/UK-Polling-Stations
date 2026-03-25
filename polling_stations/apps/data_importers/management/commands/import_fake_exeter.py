from pathlib import Path

from addressbase.models import UprnToCouncil
from core.opening_times import OpeningTimes
from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter
from data_importers.mixins import AdvanceVotingMixin
from django.contrib.gis.geos import Point
from pollingstations.models import AdvanceVotingStation


def make_base_folder_path():
    base_folder_path = Path.cwd() / Path("test_data/pollingstations_data/EXE")
    return str(base_folder_path)


class Command(BaseXpressDemocracyClubCsvImporter, AdvanceVotingMixin):
    local_files = True
    base_folder_path = make_base_folder_path()
    council_id = "EXE"
    addresses_name = "Democracy_Club__02May2019exe.CSV"
    stations_name = "Democracy_Club__02May2019exe.CSV"
    elections = ["2026-05-07"]

    def add_advance_voting_stations(self):
        opening_times = OpeningTimes()
        opening_times.add_open_time("2026-04-30", "10:00", "16:00")
        opening_times.add_open_time("2026-05-01", "10:00", "16:00")

        advance_station = AdvanceVotingStation(
            name="Exeter Guildhall",
            address="""Exeter City Council
            Civic Centre
            Paris Street
            Exeter
            Devon
            """,
            postcode="EX1 1JN",
            location=Point(-3.5245510056787057, 50.72486002944331, srid=4326),
            opening_times=opening_times.as_string_table(),
            council=self.council,
        )
        advance_station.save()
        advance_station2 = AdvanceVotingStation(
            name="Exeter Library",
            address="""Library
            Castle St
            Exeter
            """,
            postcode="EX4 3PQ",
            location=Point(-3.5406333, 50.7295503, srid=4326),
            opening_times=opening_times.as_string_table(),
            council=self.council,
        )
        advance_station2.save()
        uprn_ids = UprnToCouncil.objects.filter(
            lad=self.council.geography.gss
        ).values_list("uprn", flat=True)
        for station in [advance_station, advance_station2]:
            self.assign_advance_voting_stations(station, uprn_ids)
