from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BPL"
    addresses_name = (
        "2024-07-04/2024-06-21T14:35:52.301348/Democracy_Club__04July2024.CSV"
    )
    stations_name = (
        "2024-07-04/2024-06-21T14:35:52.301348/Democracy_Club__04July2024.CSV"
    )
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")
        if uprn in [
            "10000109140",  # 1 WINDMILL MOBILE HOME PARK PRESTON NEW ROAD, BLACKPOOL
            "10000109142",  # 2 WINDMILL MOBILE HOME PARK PRESTON NEW ROAD, BLACKPOOL
            "100010810222",  # 2 JEPSON WAY, BLACKPOOL
            "10090937406",  # FLAT 3, 128 CENTRAL DRIVE, BLACKPOOL
        ]:
            return None
        if record.addressline6 in [
            # splits
            "FY4 3DJ",
            "FY4 1HU",
        ]:
            return None

        return super().address_record_to_dict(record)
