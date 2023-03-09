from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MAL"
    addresses_name = (
        "2023-05-04/2023-03-09T19:29:09.367982/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-09T19:29:09.367982/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10094633716",  # PARK HOUSE MALDON ROAD, LATCHINGDON
            "200000910329",  # ROSEWOOD LODGE, HOWE GREEN ROAD, PURLEIGH, CHELMSFORD
        ]:
            return None

        if record.addressline6.strip() in [
            "CM9 4RA",  # confusing
            # split
            "CM9 8RU",
            "CM9 4NY",
            "CM9 6YN",
            "CM8 3LS",
            "CM9 6QP",
        ]:
            return None

        return super().address_record_to_dict(record)
