from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RDB"
    addresses_name = (
        "2021-04-19T10:11:20.029316/Redbridge Democracy_Club__06May2021.CSV"
    )
    stations_name = "2021-04-19T10:11:20.029316/Redbridge Democracy_Club__06May2021.CSV"
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10093036996",  # 40A STANLEY ROAD, ILFORD
            "10094821359",  # 705C HIGH ROAD, ILFORD
            "10094821358",  # FLAT 2, 705B HIGH ROAD, ILFORD
            "10094821357",  # FLAT 1, 705B HIGH ROAD, ILFORD
            "10094819765",  # 5 PORTLAND TERRACE, ILFORD
            "10094820912",  # 6 PORTLAND TERRACE, ILFORD
            "10093040462",  # 366B HORNS ROAD, ILFORD
            "100022231842",  # 13 PERTH ROAD, ILFORD
        ]:
            return None

        if record.addressline6 in [
            "IG5 0QA",
            "IG8 8PP",
            "E18 1ED",
            "RM6 4JF",
            "IG1 4SS",
            "IG3 8DN",
            "IG1 1QF",
            "IG1 2FP",
            "IG1 4EL",
            "IG5 0FF",
            "IG6 3FA",
        ]:
            return None

        return super().address_record_to_dict(record)
