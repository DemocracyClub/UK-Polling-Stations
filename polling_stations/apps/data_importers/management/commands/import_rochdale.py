from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RCH"
    addresses_name = (
        "2026-05-07/2026-03-06T14:11:59.587542/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-06T14:11:59.587542/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "23040672",  # NADEN HOUSE, WOODHOUSE LANE, ROCHDALE
            "23000844",  # HIGHER BROADFIELD FARM, PILSWORTH ROAD, HEYWOOD, OL10 2TA
            "10094361529",  # APPLE COTTAGE 105 SHAW ROAD, ROCHDALE, OL16 4SH
            "10094361530",  # 107 SHAW ROAD, ROCHDALE, OL16 4SH
            "10023364058",  # 1A WEST STREET, MILNROW, ROCHDALE, OL16 3BL
            "23050342",  # 2 CHADWICK STREET, FIRGROVE, ROCHDALE, OL16 3BX
            "10094362558",  # 9A YORK STREET, HEYWOOD, OL10 4NN
            "23038039",  # 81 BAGSLATE MOOR ROAD, ROCHDALE, OL11 5YH
            "23038961",  # FERN COTTAGE, BAGSLATE MOOR ROAD, ROCHDALE, OL11 5YH
            "23085791",  # LOWER STARRING FARM, STARRING ROAD, LITTLEBOROUGH, OL15 8HN
            "23090994",  # 9 TOWNHOUSE FLATS, CARRIAGE DRIVE, LITTLEBOROUGH, OL15 9AG
        ]:
            return None

        if record.post_code in [
            # splits
            "OL15 0JH",
            "M24 2PR",
            "OL11 3AE",
            "OL16 1FD",
            "OL15 0BH",
            "OL16 4XF",
            "OL10 3LW",
            "OL10 2JP",
            "OL16 2SD",
            "OL10 3BJ",
            "OL10 1FH",
            "OL15 9LY",
            "OL11 3BG",
            "M24 1LG",
            "M24 6UE",
            "OL16 4RF",
            # looks wrong
            "OL12 9BA",
            "OL15 9AU",
            "OL11 5XD",
            "OL10 1FU",
            "OL11 3FW",
            "OL12 6GP",
            "OL16 1DT",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Ignore below, address is correct
        # WARNING: Polling station Room At Rear of St James Church (6558) is in Oldham Metropolitan Borough Council (OLD)

        # postcode correction for: River Beal Cafe, River Beal Court, 14 Ladybarn Lane, Milnrow, Rochdale, OL16 4G
        if record.polling_place_id == "6885":
            record = record._replace(polling_place_postcode="OL16 4GQ")

        return super().station_record_to_dict(record)
