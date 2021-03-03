from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "ISL"
    addresses_name = "2021-03-02T14:57:29.698707/Democracy_Club__06May2021.csv"
    stations_name = "2021-03-02T14:57:29.698707/Democracy_Club__06May2021.csv"
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if record.addressline6 in [
            "N1 8LU",
            "N7 9RE",
            "EC1V 9AE",
            "N7 9RB",
            "N5 1HP",
            "N1 1NY",
            "N7 6LJ",
        ]:
            return None

        if uprn in [
            "5300090455",  # 84 THORNHILL ROAD, LONDON
        ]:
            return None

        return super().address_record_to_dict(record)
