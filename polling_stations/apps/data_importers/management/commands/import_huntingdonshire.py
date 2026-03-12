from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HUN"
    addresses_name = (
        "2026-05-07/2026-03-12T12:24:10.715270/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-12T12:24:10.715270/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10094923984",  # 3A CONEYGEAR ROAD, HARTFORD, HUNTINGDON, PE29 1QL
        ]:
            return None

        if record.addressline6 in [
            # split
            "PE28 2QG",
            "PE19 1HW",
            # looks wrong
            "PE26 1AB",
        ]:
            return None

        return super().address_record_to_dict(record)
