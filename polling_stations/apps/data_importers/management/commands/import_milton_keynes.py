from addressbase.models import UprnToCouncil
from core.opening_times import OpeningTimes
from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter
from data_importers.mixins import AdvanceVotingMixin
from pollingstations.models import AdvanceVotingStation
from django.contrib.gis.geos import Point


class Command(BaseXpressDemocracyClubCsvImporter, AdvanceVotingMixin):
    council_id = "MIK"
    addresses_name = (
        "2026-05-07/2026-03-18T12:11:48.633839/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-18T12:11:48.633839/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # splits
            "MK14 6DL",
            "MK2 2FB",
            "MK4 4EL",
            "MK13 9DZ",
            "MK46 4JS",
            "MK13 7NH",
            "MK4 4AG",
        ]:
            return None

        return super().address_record_to_dict(record)

    def add_advance_voting_stations(self):
        # https://www.milton-keynes.gov.uk/your-council-and-elections/elections-and-register-vote/central-voting-hub-trial
        opening_times = OpeningTimes()
        opening_times.add_open_time("2026-05-07", "07:00", "10:00")

        midsummer_place_advance_station = AdvanceVotingStation(
            name="Midsummer Place Shopping Centre",
            address="""Midsummer Place,
            Central Milton Keynes
            """,
            postcode="MK9 3GB",
            location=Point(-0.7564626, 52.0411655, srid=4326),
            opening_times=opening_times.as_string_table(),
            council=self.council,
        )
        midsummer_place_advance_station.save()

        # Assign all UPRNs to midsummer place
        uprn_ids = UprnToCouncil.objects.filter(
            lad=self.council.geography.gss
        ).values_list("uprn", flat=True)

        self.assign_advance_voting_stations(midsummer_place_advance_station, uprn_ids)
