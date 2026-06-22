from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RCH"
    addresses_name = (
        "2026-07-30/2026-06-22T14:25:19.621107/Democracy_Club__30July2026.tsv"
    )
    stations_name = (
        "2026-07-30/2026-06-22T14:25:19.621107/Democracy_Club__30July2026.tsv"
    )
    elections = ["2026-07-30"]
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
            "10096505235",  # HELLIWELL HOUSE, BUCKLEY HILL LANE, MILNROW, ROCHDALE
        ]:
            return None

        if record.post_code in [
            # splits
            "M24 1LG",
            "M24 2PR",
            "M24 6UE",
            "OL10 1FH",
            "OL10 2JP",
            "OL10 3BJ",
            "OL10 3LW",
            "OL11 3AE",
            "OL11 3BG",
            "OL12 0EG",
            "OL15 0BH",
            "OL15 0JH",
            "OL15 9LY",
            "OL16 1FD",
            "OL16 2SD",
            "OL16 4RF",
            "OL16 4XF",
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
