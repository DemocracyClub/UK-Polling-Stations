from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BPL"
    addresses_name = (
        "2024-05-02/2024-03-25T14:22:10.220217/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-25T14:22:10.220217/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10000109140",  # 1 WINDMILL MOBILE HOME PARK PRESTON NEW ROAD, BLACKPOOL
            "10000109142",  # 2 WINDMILL MOBILE HOME PARK PRESTON NEW ROAD, BLACKPOOL
            "10070847268",  # 89A HOLMFIELD ROAD, BLACKPOOL
            "100010797546",  # 519 DEVONSHIRE ROAD, BISPHAM, BLACKPOOL
            "100012612017",  # BLACKPOOL PARK GOLF CLUB, NORTH PARK DRIVE, BLACKPOOL
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
