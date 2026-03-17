from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "REI"
    addresses_name = (
        "2026-05-07/2026-03-17T12:17:02.474701/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-17T12:17:02.474701/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.lstrip("0")

        if uprn in [
            "68137043",  # 170 DOVERS GREEN ROAD, REIGATE
            "68137147",  # 168 DOVERS GREEN ROAD, REIGATE
        ]:
            return None

        if record.addressline6 in [
            "RH6 7HD",
        ]:
            return None

        return super().address_record_to_dict(record)
