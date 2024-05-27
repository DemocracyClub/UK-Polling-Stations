from addressbase.models import UprnToCouncil
from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BAB"
    addresses_name = (
        "2024-07-04/2024-05-27T10:31:55.894833/BMSDC PD Code data 270524.csv"
    )
    stations_name = (
        "2024-07-04/2024-05-27T10:31:55.894833/BMSDC Polling station data 270524.csv"
    )
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
            # WATTISHAM FLYING STATION, WATTISHAM AIRFIELD, IPSWICH IP7 7RA
            if record.uprn == "10094144281":
                continue
            if record.uprn in council_uprns:
                self.COUNCIL_STATIONS.add(record.stationcode)

    def station_record_to_dict(self, record):
        if record.stationcode not in self.COUNCIL_STATIONS:
            return None

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.stationcode not in self.COUNCIL_STATIONS:
            return None

        if record.uprn in [
            "10094142009",  # GREYCOTE RODBRIDGE HILL, LONG MELFORD
            "10093344109",  # 25 WAKELIN CLOSE, GREAT CORNARD, SUDBURY
            "10033308582",  # 37B WALNUT TREE LANE, SUDBURY
            "100091457209",  # KINGSBURY HOUSE, UPPER ROAD, LITTLE CORNARD, SUDBURY
            "10094140064",  # ELM VIEW, STONE STREET, HADLEIGH, IPSWICH
            "10093344041",  # 10 GRACE FARRANT ROAD, GREAT CORNARD, SUDBURY
        ]:
            return None

        if record.postcode in [
            # split
            "CO10 9LN",
            # suspect
            "CO10 2PQ",
        ]:
            return None

        return super().address_record_to_dict(record)
