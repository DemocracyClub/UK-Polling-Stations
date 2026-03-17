from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "EHA"
    addresses_name = (
        "2026-05-07/2026-03-17T10:02:53.412815/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-17T10:02:53.412815/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "1710037869",  # BRIDGE MILL, MILL LANE, PETERSFIELD
                "10094122558",  # THE LITTLE BARN, WOODSIDE FARM, GOSPORT ROAD, PRIVETT, ALTON
                "10032905833",  # ANNEXE THE HOPKILN FRITH END ROAD, FRITH END, BORDON
                "10094123612",  # WATERCRESS COTTAGE, STATION ROAD, BENTLEY, FARNHAM
                "10094121538",  # THE STABLES, COLDREY FARM, LOWER FROYLE, ALTON
                "10009812215",  # THE LITTLE BARN, WOODSIDE FARM, GOSPORT ROAD, PRIVETT, ALTON
                "10094121982",  # TREESIDE VIEW, THE SHRAVE, FOUR MARKS, ALTON
                "10094123735",  # OAK LODGE, SELBORNE ROAD, ALTON
                "10032905135",  # HALF ACRE, HAWKLEY ROAD, LISS
                "10009812211",  # THE COTTAGE, LOWER BORDEAN, BORDEAN, PETERSFIELD
                "10032907288",  # KITCOMBE BARN, KITCOMBE LANE, FARRINGDON, ALTON
                "1710109658",  # THE HERMITAGE, HEADLEY HILL ROAD, HEADLEY, BORDON
                "100060265307",  # HIGHMEAD HOUSE, OLD ODIHAM ROAD, ALTON
                "100060265308",  # HIGHMEAD COTTAGE, OLD ODIHAM ROAD, ALTON
                "10094122604",  # CORNFLOWERS, DUNSELLS LANE, ROPLEY, ALRESFORD
                "100060271325",  # RIVERSIDE, HOLLYWATER ROAD, BORDON
                "10032907889",  # ROYAL MILITARY POLICE, KITCHENER HOUSE, LONGMOOR, LISS
            ]
        ):
            return None

        if record.addressline6 in [
            # splits
            "GU33 7BL",
            "GU33 7BB",
            "PO8 0QR",
            "GU30 7QL",
            # suspect
            "GU34 3BS",
            "PO8 0RZ",
            "GU35 0UP",
            "GU35 0YU",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # add missing postcode for: Guide Headquarters, Alderfield, Borough Road, Petersfield
        if record.polling_place_id == "16364":
            record = record._replace(polling_place_postcode="GU32 3LH")

        return super().station_record_to_dict(record)
