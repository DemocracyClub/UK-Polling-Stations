from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "PRE"
    addresses_name = (
        "2025-05-01/2025-03-05T11:23:25.390587/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-05T11:23:25.390587/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10007606520",  # WILLOW BANK, INGLEWHITE ROAD, GOOSNARGH, PRESTON
            "100010579401",  # 16A WOODPLUMPTON ROAD, ASHTON-ON-RIBBLE, PRESTON
            "100010574023",  # 219 TULKETH BROW, ASHTON-ON-RIBBLE, PRESTON
            "100012402901",  # MEADOWBROOK, INGLEWHITE ROAD, GOOSNARGH, PRESTON
            "100012401519",  # INGLENOOK BARN, CARRON LANE, INGLEWHITE, PRESTON
            "100012405502",  # 105A WHITTINGHAM LANE, BROUGHTON, PRESTON
            "10013339494",  # SIMPSON HOUSE, FERNYHALGH LANE, FULWOOD, PRESTON
            "100010534827",  # BARBER SHOP, 109A BLACK BULL LANE, FULWOOD, PRESTON
            "10093760272",  # 17 BLYTHE ROAD, LIGHTFOOT GREEN, PRESTON
            "10090426536",  # 236A RIBBLETON LANE, PRESTON
            "10090427208",  # 135 SKEFFINGTON ROAD, PRESTON
            "10090427211",  # FLAT 2 135A SKEFFINGTON ROAD, PRESTON
            "10090427212",  # FLAT 3 135A SKEFFINGTON ROAD, PRESTON
            "10090427213",  # FLAT 4 135A SKEFFINGTON ROAD, PRESTON
            "10090427210",  # FLAT 1 135A SKEFFINGTON ROAD, PRESTON
            "100010538499",  # 4 CEMETERY ROAD, PRESTON
            "100010538500",  # 5 CEMETERY ROAD, PRESTON
            "100010538498",  # 3 CEMETERY ROAD, PRESTON
            "100010538497",  # 2 CEMETERY ROAD, PRESTON
            "100010538496",  # 1 CEMETERY ROAD, PRESTON
            "100012746089",  # 119 OXFORD STREET, PRESTON
            "10093760392",  # 48 CHELTENHAM CRESCENT, LIGHTFOOT GREEN, PRESTON
        ]:
            return None

        if record.addressline6 in [
            # looks wrong
            "PR1 3SG",
            "PR2 5PZ",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Millennium Hall, Neapsands Close, Fulwood, Preston, PR2 9AQ
        if record.polling_place_id == "5109":
            record = record._replace(
                polling_place_easting="355831", polling_place_northing="432404"
            )

        return super().station_record_to_dict(record)
