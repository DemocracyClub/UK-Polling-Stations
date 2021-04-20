from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SHA"
    addresses_name = (
        "2021-03-31T10:24:27.847767/South Hams Democracy_Club__06May2021.tsv"
    )
    stations_name = (
        "2021-03-31T10:24:27.847767/South Hams Democracy_Club__06May2021.tsv"
    )
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if record.addressline6 in ["TQ7 3LW", "TQ11 0JT"]:
            return None
        #
        if uprn in [
            "10008857241",  # long distance; embedded in another district
        ]:
            return None

        return rec
