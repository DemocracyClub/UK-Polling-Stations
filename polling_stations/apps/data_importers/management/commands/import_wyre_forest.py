from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WYE"
    addresses_name = "2021-03-29T13:16:10.236797/Democracy_Club__06May2021.tsv"
    stations_name = "2021-03-29T13:16:10.236797/Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10003382058",  # THE PATCH, LEIGHT LANE, RIBBESFORD, BEWDLEY
        ]:
            return None

        if record.addressline6 in [
            "DY12 2TN",
            "DY10 3HJ",
            "DY10 2QD",
            "DY10 3TF",
            "DY11 5QT",
            "DY10 3HH",
            "DY10 1SB",
            "DY10 1LS",
            "DY10 3EL",
        ]:
            return None

        return super().address_record_to_dict(record)
