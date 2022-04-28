from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "PLY"
    addresses_name = (
        "2022-05-05/2022-04-28T18:58:10.618180/Democracy_Club__05May2022v2.tsv"
    )
    stations_name = (
        "2022-05-05/2022-04-28T18:58:10.618180/Democracy_Club__05May2022v2.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10070771403",
            "10070771404",
            "100040493091",
            "100040429061",
        ]:
            return None

        if record.addressline6 in [
            "PL3 6EP",
            "PL4 7QB",
            "PL6 5JZ",
        ]:
            return None

        return super().address_record_to_dict(record)
