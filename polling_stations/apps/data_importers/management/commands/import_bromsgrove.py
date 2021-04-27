from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BRM"
    addresses_name = "2021-04-23T10:43:51.069438/Democracy_Club__06May2021Broms.CSV"
    stations_name = "2021-04-23T10:43:51.069438/Democracy_Club__06May2021Broms.CSV"
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100120585529",  # 35 CHERRY HILL ROAD, BARNT GREEN, BIRMINGHAM
            "10090741909",  # THE OLD FORGE, BROMSGROVE ROAD, CLENT, STOURBRIDGE
        ]:
            return None

        if record.addressline6 in [
            "B60 3AZ",
            "B61 7AY",
            "B61 0NX",
            "B47 6LX",
            "B45 8HY",
            "B60 1QG",
        ]:
            return None

        return super().address_record_to_dict(record)
