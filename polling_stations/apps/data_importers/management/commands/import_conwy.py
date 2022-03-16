from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CWY"
    addresses_name = (
        "2022-05-05/2022-03-16T08:47:19.437583/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-16T08:47:19.437583/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "LL24 0LP",
            "LL26 0YU",
            "LL31 9EQ",
            "LL30 1YQ",
            "LL30 1NT",
            "LL22 7DT",
            "LL21 9PH",
            "LL32 8HW",
            "LL22 8FB",
        ]:
            return None

        if record.property_urn.lstrip(" 0") in [
            "10023132438",
        ]:
            return None

        return super().address_record_to_dict(record)
