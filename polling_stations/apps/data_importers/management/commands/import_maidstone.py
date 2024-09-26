from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MAI"
    addresses_name = (
        "2024-07-04/2024-05-30T15:24:34.390824/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-05-30T15:24:34.390824/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "10093304076",  # 25 MEADOW VIEW, PILGRIMS RETREAT, HARRIETSHAM, MAIDSTONE
                "10093304077",  # 26 MEADOW VIEW, PILGRIMS RETREAT, HARRIETSHAM, MAIDSTONE
                "10093304078",  # 27 MEADOW VIEW, PILGRIMS RETREAT, HARRIETSHAM, MAIDSTONE
                "10093304078",  # THE FARMHOUSE, LITTLE BENOVER, BENOVER ROAD, YALDING, MAIDSTONE
            ]
        ):
            return None
        if record.addressline6 in [
            # split
            "ME15 6EL",
            "ME16 8DT",
            "ME15 9RA",
            "ME14 3EP",
            # suspect
            "ME18 5EF",
            "ME18 5ED",
        ]:
            return None
        return super().address_record_to_dict(record)
