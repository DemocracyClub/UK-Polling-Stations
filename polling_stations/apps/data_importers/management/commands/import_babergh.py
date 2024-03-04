from addressbase.models import UprnToCouncil
from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BAB"
    addresses_name = (
        "2024-05-02/2024-02-27T18:05:23.830024/BMSDC Polling Districts extract.csv"
    )
    stations_name = (
        "2024-05-02/2024-02-27T18:05:23.830024/BMSDC Polling Station extract.csv"
    )
    elections = ["2024-05-02"]
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
        # Polstead Village Hall, Polstead Green CO6 5AN
        if record.stationcode == "B13":
            record = record._replace(xordinate="599265")
            record = record._replace(yordinate="238341")
            record = record._replace(postcode="CO6 5AL")

        # Belstead Brook Muthu Hotel, Belstead Road, Ipswich IP2 9HB
        if record.stationcode == "B70":
            record = record._replace(xordinate="614333")
            record = record._replace(yordinate="242067")

        # Address: Stoke by Nayland Village Hall, Church Street, Stoke By Nayland CO6 4QP
        if record.stationcode == "B17":
            record = record._replace(xordinate="598791")
            record = record._replace(yordinate="236256")

        # Polstead Village Hall, Polstead Green CO6 5AN
        if record.stationcode == "B30":
            record = record._replace(xordinate="610047")
            record = record._replace(yordinate="234752")

        # The Pavillion, Hadleigh Cricket Club, Friars Road, Hadleigh IP7 5BH
        if record.stationcode == "B38":
            record = record._replace(postcode="IP7 6DF")

        # Change from council:
        # Old station: Raydon Village Hall, Hadleigh Road, Raydon IP7 5LH
        # New station: King George's Field and Sports Pavilion, The Street, Raydon IP7 5LT
        if record.stationcode == "B14":
            record = record._replace(
                placename="King George's Field and Sports Pavilion",
                add1="The Street",
                postcode="IP7 5LT",
                xordinate="",
                yordinate="",
            )
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
            "CO10 9LN",  # split
            "CO10 2PQ",  # suspect
        ]:
            return None

        return super().address_record_to_dict(record)
