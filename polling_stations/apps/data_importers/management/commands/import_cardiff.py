from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):

    council_id = "CRF"
    addresses_name = "2021-03-24T16:24:49.782410/cardiff_deduped.tsv"
    stations_name = "2021-03-24T16:24:49.782410/cardiff_deduped.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "100100110392":
            return None

        if record.addressline6 in [
            "CF24 3DZ",
            "CF3 0UH",
            "CF14 2FN",
            "CF14 6PE",
            "CF24 4RU",
            "CF3 4LL",
            "CF5 6HF",
            "CF14 9UA",
        ]:
            return None

        return super().address_record_to_dict(record)
