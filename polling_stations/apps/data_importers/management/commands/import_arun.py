from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "ARU"
    addresses_name = (
        "2024-07-04/2024-06-04T17:13:04.887420/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-04T17:13:04.887420/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100061686788",  # SOUTHDOWN COTTAGE, YAPTON LANE, WALBERTON, ARUNDEL
            "100061698125",  # 1 KINGSWAY, BOGNOR REGIS
        ]:
            return None

        if record.addressline6 in [
            # splits
            "PO21 1JB",
            # looks wrong
            "PO22 8GE",
            "PO22 8GD",
            "PO22 8GF",
            "PO22 8GB",
            "PO22 8GQ",
            "PO22 8GP",
        ]:
            return None

        return super().address_record_to_dict(record)
