from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "EAS"
    addresses_name = "2024-07-04/2024-05-30T15:12:16.711971/Eros_SQL_Output001.csv"
    stations_name = "2024-07-04/2024-05-30T15:12:16.711971/Eros_SQL_Output001.csv"
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10010654823",  # FLAT 2 16A SILVERDALE ROAD, EASTBOURNE
            "10010662297",  # 141 WILLINGDON ROAD, EASTBOURNE
            "10010654824",  # FLAT 1 16A SILVERDALE ROAD, EASTBOURNE
            "100062252513",  # GRANGE HOUSE, 21 GRANGE ROAD, EASTBOURNE
            "100062248097",  # 2A SILVERDALE ROAD, EASTBOURNE
            "10010661217",  # STAFF FLAT THE GRAND HOTEL KING EDWARDS PARADE, EASTBOURNE
            "10010663120",  # MANANGERS FLAT THE STAGE DOOR 10 COMPTON STREET, EASTBOURNE
            "10010652269",  # PUPIL ACCOMMODATION THE SCHOOL HOUSE COLLEGE ROAD, EASTBOURNE
            "10093962387",  # HOUSE MASTERS FLAT, BLACKWATER HOUSE 19A, GRANGE ROAD, EASTBOURNE
            "10010661434",  # 1 HAMPDEN PARK DRIVE, EASTBOURNE
            "100061912921",  # SUMMERDOWN FARM COTTAGE, DOWNS VIEW LANE, EAST DEAN, EASTBOURNE
            "100060014635",  # MILTON GRANGE, MILTON ROAD, EASTBOURNE
            "100060022728",  # 5 THE GOFFS, EASTBOURNE
            "10010651086",  # RINGWOOD FARM, EAST DEAN ROAD, EAST DEAN, EASTBOURNE
            "100060004020",  # 11A CAREW ROAD, EASTBOURNE
            "10093962377",  # 11B CAREW ROAD, EASTBOURNE
            "10093962378",  # LAVENDER COTTAGE 11C CAREW ROAD, EASTBOURNE
        ]:
            return None

        if record.housepostcode in [
            # split
            "BN20 8DP",
            "BN23 8JH",
            # suspect
            "BN20 7BL",  # TULLOCH HOUSE, 6 CARLISLE ROAD, EASTBOURNE
            "BN23 7PB",  # LANGNEY VILLAS, 168 LANGNEY RISE, EASTBOURNE
            "BN23 8AG",  # FRIDAY STREET, EASTBOURNE
            "BN21 2HD",  # ARUNDEL ROAD, EASTBOURNE
        ]:
            return None
        return super().address_record_to_dict(record)
