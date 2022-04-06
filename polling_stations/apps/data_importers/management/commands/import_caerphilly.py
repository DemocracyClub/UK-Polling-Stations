from addressbase.models import Address, UprnToCouncil
from core.opening_times import OpeningTimes
from data_importers.management.commands import BaseHalaroseCsvImporter
from data_importers.mixins import AdvanceVotingMixin
from pollingstations.models import AdvanceVotingStation


class Command(BaseHalaroseCsvImporter, AdvanceVotingMixin):
    council_id = "CAY"
    addresses_name = (
        "2022-05-05/2022-04-06T17:29:17.555011/polling_station_export-2022-04-06.csv"
    )
    stations_name = (
        "2022-05-05/2022-04-06T17:29:17.555011/polling_station_export-2022-04-06.csv"
    )
    elections = ["2022-05-05"]

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            "NP22 5HU",
            "NP10 9GG",
            "NP11 6JE",
            "CF83 8RL",
        ]:
            return None  # split

        return super().address_record_to_dict(record)

    def add_advance_voting_stations(self):
        opening_times = OpeningTimes()
        opening_times.add_open_time("2022-04-30", "10:00", "16:00")
        opening_times.add_open_time("2022-05-01", "10:00", "16:00")

        advance_station = AdvanceVotingStation(
            name="Council Headquarters",
            address="""Penallta House,
            Tredomen Business Park,
            Ystrad Mynach,
            Hengoed
                """,
            postcode="CF82 7PG",
            location=Address.objects.get(uprn=43164445).location,
            opening_times=opening_times.as_string_table(),
            council=self.council,
        )
        advance_station.save()
        UprnToCouncil.objects.filter(lad=self.council.geography.gss).update(
            advance_voting_station=advance_station
        )
