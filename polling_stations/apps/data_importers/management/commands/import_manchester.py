from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MAN"
    addresses_name = (
        "2026-02-26/2026-02-04T14:12:40.743599/Democracy_Club__26February2026.tsv"
    )
    stations_name = (
        "2026-02-26/2026-02-04T14:12:40.743599/Democracy_Club__26February2026.tsv"
    )
    elections = ["2026-02-26"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10093073712",
            "77176372",
        ]:
            return None

        if record.addressline6 in [
            # looks wrong
            "M19 3NW",
        ]:
            return None

        return super().address_record_to_dict(record)
