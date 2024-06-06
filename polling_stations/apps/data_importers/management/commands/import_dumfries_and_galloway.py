from addressbase.models import UprnToCouncil
from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "DGY"
    addresses_name = "2024-07-04/2024-06-26T11:17:13.719868/Democracy Club - Dumfries and Galloway Polling Districts.csv"
    stations_name = "2024-07-04/2024-06-26T11:17:13.719868/Democracy Club - Dumfries and Galloway Polling Stations.csv"
    elections = ["2024-07-04"]
    csv_encoding = "utf-16le"

    def pre_import(self):
        # We need to consider rows that don't have a uprn when importing data.
        # However there are lots of rows for other councils in this file.
        # So build a list of stations from rows that do have UPRNS
        # and then use that list of stations to make sure we check relevant rows, even if they don't have a UPRN

        council_uprns = set(
            UprnToCouncil.objects.filter(lad=self.council.geography.gss).values_list(
                "uprn", flat=True
            )
        )
        self.COUNCIL_STATIONS = set()
        data = self.get_addresses()

        for record in data:
            if record.uprn in council_uprns:
                self.COUNCIL_STATIONS.add(record.stationcode)

    def address_record_to_dict(self, record):
        if record.stationcode not in self.COUNCIL_STATIONS:
            return None
        if record.postcode in [
            # split
            "DG8 0BZ",
            "DG9 9AL",
            "DG8 6TA",
        ]:
            return None
        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        if record.stationcode not in self.COUNCIL_STATIONS:
            return None

        # MIDDLEBIE COMMUNITY CENTRE, MIDDLEBIE, LOCKERBIE
        if record.stationcode == "N0DCT048":
            record = record._replace(xordinate="")
            record = record._replace(yordinate="")

        # THORNHILL COMMUNITY CENTRE, EAST BACK STREET, THORNHILL
        if record.stationcode in [
            "N0DCT008",
            "N0DCT009",
        ]:
            record = record._replace(xordinate="")
            record = record._replace(yordinate="")
        return super().station_record_to_dict(record)
