from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SFT"
    addresses_name = (
        "2023-05-04/2023-03-18T09:10:00.674374/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-18T09:10:00.674374/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"


def address_record_to_dict(self, record):
    uprn = record.property_urn.strip().lstrip("0")

    if uprn in [
        "41063021",  # 8 MOOR LANE, THORNTON, LIVERPOOL
    ]:
        return None
    if record.addressline6 in [
        "L23 7TX",
    ]:
        return None

    return super().address_record_to_dict(record)
