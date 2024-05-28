from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "DAC"
    addresses_name = (
        "2024-07-04/2024-05-28T14:30:36.619251/Democracy_Club__04July2024.CSV"
    )
    stations_name = (
        "2024-07-04/2024-05-28T14:30:36.619251/Democracy_Club__04July2024.CSV"
    )
    elections = ["2024-07-04"]

    def station_record_to_dict(self, record):
        # more accurate point for: Nash Mills Village Hall, 4 Lower Road, Nash Mills, HP3 8RU
        if record.polling_place_id == "3036":
            record = record._replace(polling_place_easting="507211")
            record = record._replace(polling_place_northing="204366")

        # address correction for: St Pauls Church Hall, 39 Meadow Road, Hemel Hempstead, HP3 8AJ
        if record.polling_place_id == "2947":
            record = record._replace(polling_place_name="St Paul's Church")
            record = record._replace(polling_place_address_1="Solway")
            record = record._replace(polling_place_address_4="Hemel Hempstead")
            record = record._replace(polling_place_postcode="HP2 5QN")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200001852107",  # SEBRIGHT FARM, CLEMENTS END ROAD, GADDESDEN ROW, HEMEL HEMPSTEAD
            "100081181210",  # HOLLOWAY COTTAGE, HASTOE, TRING
            "10095348524",  # LAKE VIEW, PIX FARM LANE, HEMEL HEMPSTEAD
            "10093312995",  # 1 LOCKERS PARK LANE, HEMEL HEMPSTEAD
            "100080710707",  # 8 WOODFIELD GARDENS, HEMEL HEMPSTEAD
            "100080710712",  # 14 WOODFIELD GARDENS, HEMEL HEMPSTEAD
            "200004054571",  # FLAT THE YOUNG PRETENDER 37 HEMPSTEAD ROAD, KINGS LANGLEY
            "100081111251",  # WOODILL FARM, NETTLEDEN ROAD, LITTLE GADDESDEN, BERKHAMSTED
            "200001052307",  # THE COTTAGE, BULLBEGGARS LANE, BERKHAMSTED
            "100081113670",  # OLD FISHERY COTTAGE, OLD FISHERY LANE, HEMEL HEMPSTEAD
            "100081113665",  # BARGEMOOR, OLD FISHERY LANE, HEMEL HEMPSTEAD
            "100081113665",  # BARGEMOOR, OLD FISHERY LANE, HEMEL HEMPSTEAD
        ]:
            return None

        if record.addressline6 in [
            # splits
            "HP2 4AP",
            "HP2 6JN",
            # looks wrong
            "HP3 9DJ",
            "HP1 2RE",
            "HP23 5BE",
        ]:
            return None

        return super().address_record_to_dict(record)
