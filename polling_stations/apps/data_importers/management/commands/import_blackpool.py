from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BPL"
    addresses_name = (
        "2023-05-04/2023-04-21T09:57:57.018657/Democracy_Club__04May2023.CSV"
    )
    stations_name = (
        "2023-05-04/2023-04-21T09:57:57.018657/Democracy_Club__04May2023.CSV"
    )
    elections = ["2023-05-04"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10000109140",  # 1 WINDMILL MOBILE HOME PARK PRESTON NEW ROAD, BLACKPOOL
            "10070847268",  # 89A HOLMFIELD ROAD, BLACKPOOL
            "100010797546",  # 519 DEVONSHIRE ROAD, BISPHAM, BLACKPOOL
            "10008479652",  # 80 COOPERS WAY, BLACKPOOL
            "10070845204",  # FLAT 2 33 COOKSON STREET, BLACKPOOL
            "10070845203",  # FLAT 1A 33 COOKSON STREET, BLACKPOOL
            "100012612017",  # BLACKPOOL PARK GOLF CLUB, NORTH PARK DRIVE, BLACKPOOL
            "10090938672",  # 5 TAYBANK AVENUE, BLACKPOOL
            "100012614367",  # POPLAR COTTAGE, JUBILEE LANE, BLACKPOOL
            "100010810222",  # 2 JEPSON WAY, BLACKPOOL
            "100010823531",  # 130 PALATINE ROAD, BLACKPOOL
            "10090937406",  # FLAT 3, 128 CENTRAL DRIVE, BLACKPOOL
            "10090937787",  # 18 REDWOOD BOULEVARD, BLACKPOOL
        ]:
            return None

        if record.addressline6 in [
            # splits
            "FY4 3DJ",
            "FY4 1HU",
            "FY2 0WS",  # TOWER VIEW, BLACKPOOL
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # WARNING: Polling station Cleveleys Baptist Church (6061) is in Wyre Borough Council (WYR)
        # The above warning was checked, no action required
        return super().station_record_to_dict(record)
