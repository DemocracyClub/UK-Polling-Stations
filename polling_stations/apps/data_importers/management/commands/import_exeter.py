from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "EXE"
    addresses_name = "2021-03-23T11:45:52.642475/Exeter Democracy_Club__06May2021.CSV"
    stations_name = "2021-03-23T11:45:52.642475/Exeter Democracy_Club__06May2021.CSV"
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10091473295",  # EXE VIEW LODGE STOKE HILL, EXETER
            "100041124933",  # THE GRANGE, HARTS LANE, EXETER
        ]:
            return None

        if record.addressline6 in [
            "EX4 5AJ",
            "EX2 7AY",
            "EX2 7TF",
            "EX4 1RD",
            "EX4 9HE",
            "EX4 1AS",
            "EX2 8DQ",
            "EX1 3FA",
        ]:
            return None

        return super().address_record_to_dict(record)
