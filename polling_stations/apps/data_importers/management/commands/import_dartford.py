from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "DAR"
    addresses_name = "2021-03-12T12:25:27.291565/polling_station_export-2021-03-12.csv"
    stations_name = "2021-03-12T12:25:27.291565/polling_station_export-2021-03-12.csv"
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10094156345",  # 447A PRINCES ROAD, DARTFORD
            "200000533812",  # THE NOOK, POWDER MILL LANE, DARTFORD
            "200000538710",  # THE COACH HOUSE, HAWLEY ROAD, DARTFORD
        ]:
            return None

        if record.housepostcode in ["DA9 9XT"]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):

        # 8th Dartford Scout Hall (PRI5) Oakfield Lane Dartford Kent DA1 2EU and
        # 8th Dartford Scout Hall (WSH5) Oakfield Lane Dartford Kent DA1 2EU
        if "8th Dartford Scout Hall" in record.pollingstationname:
            record = record._replace(pollingstationpostcode="DA1 2SP")

        return super().station_record_to_dict(record)
