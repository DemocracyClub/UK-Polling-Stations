from addressbase.models import Address, UprnToCouncil
from core.opening_times import OpeningTimes
from data_importers.management.commands import BaseHalaroseCsvImporter
from data_importers.mixins import AdvanceVotingMixin
from pollingstations.models import AdvanceVotingStation


class Command(BaseHalaroseCsvImporter, AdvanceVotingMixin):
    council_id = "BGW"
    addresses_name = (
        "2022-05-05/2022-03-21T12:39:42.933221/polling_station_export-2022-03-21.csv"
    )
    stations_name = (
        "2022-05-05/2022-03-21T12:39:42.933221/polling_station_export-2022-03-21.csv"
    )
    elections = ["2022-05-05"]
    csv_encoding = "windows-1252"

    def station_record_to_dict(self, record):
        if record.pollingstationnumber in [
            "61",  # EBENEZER CHAPEL VESTRY
        ]:
            record = record._replace(pollingstationpostcode="NP22 4RQ")
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):

        if record.housepostcode in [
            "NP23 5DH",
            "NP13 3JU",
            "NP13 3AQ",
        ]:
            return None

        return super().address_record_to_dict(record)

    def add_advance_voting_stations(self):
        opening_times = OpeningTimes()
        opening_times.add_open_time("2022-05-03", "08:00", "16:00")
        opening_times.add_open_time("2022-05-04", "08:00", "16:00")

        advance_station = AdvanceVotingStation(
            name="Ebbw Vale Learning Zone",
            address="""Lime Avenue
            Ebbw Vale
                """,
            postcode="NP23 6GL",
            location=Address.objects.get(uprn="10014120799").location,
            opening_times=opening_times.as_string_table(),
            council=self.council,
        )
        advance_station.save()
        UprnToCouncil.objects.filter(lad=self.council.geography.gss).update(
            advance_voting_station=advance_station
        )
