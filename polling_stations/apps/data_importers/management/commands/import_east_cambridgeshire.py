from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "ECA"
    addresses_name = (
        "2024-07-04/2024-06-14T16:11:50.619064/Democracy Club - Polling Districts.csv"
    )
    stations_name = (
        "2024-07-04/2024-06-14T16:11:50.619064/Democracy Club - Polling Stations.csv"
    )
    elections = ["2024-07-04"]
    csv_encoding = "utf-16le"

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")
        if uprn in [
            "100090041333",  # 15 BLACK BANK ROAD, LITTLE DOWNHAM, ELY
            "100090041332",  # 17 BLACK BANK ROAD, LITTLE DOWNHAM, ELY
            "10095400067",  # 163 THE STREET, KIRTLING, NEWMARKET
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Below warnings checked and no correction needed:
        # Polling station NEWMARKET TOWN FOOTBALL CLUB - CHEVELEY (MD1) is in West Suffolk Council (WSK)
        # Polling station NEWMARKET TOWN FOOTBALL CLUB - WOODDITTON (MJ1) is in West Suffolk Council (WSK)

        # Remove stations from SCA council
        if record.stationcode in [
            "OB1",
            "OC1",
            "OC1,OC2",
            "OD1/1",
            "OD2",
            "SA1/1",
            "SC1",
        ]:
            return None

        return super().station_record_to_dict(record)
