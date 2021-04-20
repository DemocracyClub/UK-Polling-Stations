from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MON"
    addresses_name = "2021-04-09T11:13:40.300549/Democracy_Club__06May2021.tsv"
    stations_name = "2021-04-09T11:13:40.300549/Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6.strip() in [
            "NP7 7DH",
            "NP7 7EE",
            "NP7 7HU",
            "NP7 7DW",
            "NP7 5LL",
            "NP7 5LF",
            "NP7 5LB",
            "NP7 6AN",
            "NP7 5SS",
            "NP26 5NS",
            "NP26 3AR",
            "NP16 6HX",
            "NP16 6JS",
            "NP16 5JF",
            "NP16 6RQ",
            "NP7 8NL",
            "NP15 1NP",
            "NP7 9UL",
            "NP7 9EG",
            "NP15 1PY",
            "NP7 0LL",
            "NP7 0EY",
            "NP7 9HT",
            "NP7 7EY",
            "NP7 9BT",
            "NP7 9EU",
            "NP25 5DJ",
            "NP25 5EJ",
            "NP25 5BG",
            "NP25 3LP",
            "NP25 5AP",
            "NP25 4BP",
            "NP25 4TS",
        ]:
            return None  # split

        if (
            record.addressline6 == "NP25 4BG"
            and record.polling_place_district_reference == "9458"
        ):
            return None  # far from other properties in this area

        if record.property_urn.strip(" 0") in [
            "10033355660",
            "10033360145",
            "10033346790",
            "10033356456",
            "10033348014",
            "10033355660",
            "10033339048",
        ]:
            return None  # far from other properties in this area

        return super().address_record_to_dict(record)
