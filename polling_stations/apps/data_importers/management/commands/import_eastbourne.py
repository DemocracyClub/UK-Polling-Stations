from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "EAS"
    addresses_name = "2021-03-04T10:47:15.541961/Eastbourne Borough polling_station_export-2021-03-04.csv"
    stations_name = "2021-03-04T10:47:15.541961/Eastbourne Borough polling_station_export-2021-03-04.csv"
    elections = ["2021-05-06"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if record.housepostcode in ["BN22 7HL", "BN20 8EJ", "BN20 7AU", "BN20 8TL"]:
            return None

        if uprn in [
            "10010662297",
            "10024142453",
            "10093961546",
        ]:
            return None

        return super().address_record_to_dict(record)
