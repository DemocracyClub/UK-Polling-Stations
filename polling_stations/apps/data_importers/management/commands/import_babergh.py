from addressbase.models import UprnToCouncil
from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BAB"
    addresses_name = "2024-07-04/2024-05-24T12:37:03.753159/BMSDC PD Code data.csv"
    stations_name = (
        "2024-07-04/2024-05-24T12:37:03.753159/BMSDC Polling station data.csv"
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

        # Burstall Village Hall, The Street, Burstall IP8 3DY
        # Looks like it has been assigned the wrong polling district so removing it entirely for now
        if record.stationcode == "SS27":
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
            # the following look wrongly assigned:
            "IP8 3EB",
            "IP8 3EA",
            "IP8 3DY",
            "IP8 3DS",
            "IP8 3DU",
            "IP8 3ER",
            "IP8 3DW",
            "IP8 3DR",
            "IP8 3DT",
            "IP8 3EQ",
            "IP8 3DL",
            "IP8 3ES",
            "IP8 3DP",
            "IP8 3ED",
            "IP8 3DZ",
            "IP8 3DX",
            "IP8 3EE",
            "IP8 3EG",
            "IP8 3DN",
        ]:
            return None

        # Burstall Village Hall, The Street, Burstall IP8 3DY
        if record.stationcode == "SS27":
            return None

        return super().address_record_to_dict(record)
