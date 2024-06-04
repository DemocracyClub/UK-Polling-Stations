from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WIN"
    addresses_name = (
        "2024-07-04/2024-06-04T05:40:31.473736/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-04T05:40:31.473736/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")
        if uprn in [
            "200000182939",  # CARAVAN 1 POINTERS PADDOCK SHEARDLEY LANE, DROXFORD
            "200000179695",  # CARAVAN 2 POINTERS PADDOCK SHEARDLEY LANE, DROXFORD
            "10094862207",  # 3 CAMPION ROAD, CURBRIDGE
            "100062013522",  # SPRING FARM, HAMBLEDON, WATERLOOVILLE
            "10034500599",  # THE FLAT HORSE AND JOCKEY HIPLEY FAREHAM ROAD, HAMBLEDON
            "10000835251",  # WOODSIDE, BOTLEY ROAD, CURBRIDGE, SOUTHAMPTON
            "200000182727",  # BRIDGE LODGE BRIDGE FARM BOTLEY ROAD, CURBRIDGE
            "10034499812",  # PENNY ACRES, CLEWERS HILL, WALTHAM CHASE, SOUTHAMPTON
            "200000179800",  # NORTH LODGE, WINCHESTER ROAD, DURLEY, SOUTHAMPTON
            "100062518967",  # 16 LIME CLOSE, COLDEN COMMON, WINCHESTER
            "100060605297",  # 18 LIME CLOSE, COLDEN COMMON, WINCHESTER
            "10090843819",  # 41 SPRING LANE, COLDEN COMMON, WINCHESTER
            "10090843820",  # 41A SPRING LANE, COLDEN COMMON, WINCHESTER
            "100060607429",  # NORTHWOOD LODGE, NORTHWOOD PARK, SPARSHOLT, WINCHESTER
            "100060611152",  # OVERCOMBE, ST, CROSS ROAD, WINCHESTER
            "10090845084",  # FLAT 8, 4 ST, CROSS ROAD, WINCHESTER
            "100060612001",  # SILWOOD LODGE, STOCKBRIDGE ROAD, WINCHESTER
            "10094862719",  # 18 BURSTALL GARDENS, WINCHESTER
            "100060612522",  # 2 TAPLINGS ROAD, WINCHESTER
            "100060614468",  # 1 WESTMAN ROAD, WINCHESTER
            "10034499070",  # 105 WESLEY ROAD, KINGS WORTHY, WINCHESTER
            "10034499071",  # 106 WESLEY ROAD, KINGS WORTHY, WINCHESTER
            "100062011695",  # THE OLD TOLL HOUSE, THE AVENUE, ALRESFORD
            "100062527476",  # THE WILLOWS, HAMBLEDON LANE, SOBERTON, SOUTHAMPTON
            "100060590943",  # WESTWOOD COTTAGE, DROXFORD ROAD, SWANMORE, SOUTHAMPTON
            "100062526475",  # WOODMANS COTTAGE, BIDDENFIELD LANE, SHEDFIELD, SOUTHAMPTON
            "100062526472",  # SPRING COTTAGE, BIDDENFIELD LANE, SHEDFIELD, SOUTHAMPTON
            "100060587033",  # FERNDALE HOUSE, POUND HILL, ALRESFORD
            "200000179223",  # PADDOCK HOUSE GALLEY DOWN FARM, DUNDRIDGE LANE, BISHOPS WALTHAM, SOUTHAMPTON
            "100062525886",  # GALLEY DOWN FARM, DUNDRIDGE LANE, BISHOPS WALTHAM, SOUTHAMPTON
            "200000184195",  # BROCKBRIDGE COTTAGE, BROCKBRIDGE, DROXFORD, SOUTHAMPTON
            "200000179662",  # SWANMORE BARN FARM, PARK LANE, SWANMORE, SOUTHAMPTON
            "200000179475",  # PAPER MILL COTTAGE, WARNFORD, SOUTHAMPTON
            "200000184731",  # LOWER PEAKE, WARNFORD, SOUTHAMPTON
            "10094862089",  # 9 MONKS BROOK ROAD, CURBRIDGE, SOUTHAMPTON
        ]:
            return None
        if record.addressline6 in [
            # split
            "SO24 9HZ",
            "SO32 1HP",
            "SO32 3PJ",
        ]:
            return None
        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # more accurate point for: Upham New Millennium Village Hall (Cttee Room), Mortimers Lane, Lower Upham, SO32 1HF
        if record.polling_place_id == "11486":
            record = record._replace(polling_place_easting="452220")
            record = record._replace(polling_place_northing="119570")

        return super().station_record_to_dict(record)
