from django.contrib.gis.geos import Point

from addressbase.models import UprnToCouncil
from data_importers.mixins import AdvanceVotingMixin
from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter
from pathlib import Path

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

    def add_advance_voting_stations(self):
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
        )
        advance_station.save()
        UprnToCouncil.objects.filter(lad=self.council.geography.gss).update(
            advance_voting_station=advance_station
        )
