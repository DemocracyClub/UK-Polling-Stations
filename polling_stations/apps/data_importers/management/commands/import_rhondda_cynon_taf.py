from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "RCT"
    addresses_name = (
        "2025-07-17/2025-06-23T13:45:28.023964/SupportSql_20250623_111839.csv"
    )
    stations_name = (
        "2025-07-17/2025-06-23T13:45:28.023964/SupportSql_20250623_111839.csv"
    )
    elections = ["2025-07-17"]
    # by-election so maintaining previous exclusions for reference

    # def station_record_to_dict(self, record):
    #     # postcode correction for: ST DAVIDS CHURCH, LLANTRISANT ROAD, GROESFAEN, PONTYCLUN, CF72 8NU
    #     if self.get_station_hash(record) == "58-st-davids-church":
    #         record = record._replace(pollingstationpostcode="CF72 8NS")

    #     # postcode correction for: CILFYNYDD AND NORTON BRIDGE COMMUNITY CENTRE, CILFYNYDD ROAD, CILFYNYDD, PONTYPRIDD, CF37 3NR
    #     if (
    #         self.get_station_hash(record)
    #         == "121-cilfynydd-and-norton-bridge-community-centre"
    #     ):
    #         record = record._replace(pollingstationpostcode="CF37 4NR")

    #     # postcode correction for: ST LUKES CHURCH, CARDIFF ROAD, HAWTHORN, PONTYPRIDD, CF37 5LG
    #     if self.get_station_hash(record) == "138-st-lukes-church":
    #         record = record._replace(pollingstationpostcode="CF37 5LN")

    #     # adding postcode for: RHYDYFELIN LIBRARY, POPLAR ROAD, RHYDYFELIN, PONTYPRIDD
    #     if self.get_station_hash(record) == "136-rhydyfelin-library":
    #         record = record._replace(pollingstationpostcode="CF37 5LR")

    #     # The following stations postcodes have been confirmed with the council:

    #     # 'LLWYNYPIA BOYS AND GIRLS CLUB, LLWYNYPIA ROAD, TONYPANDY, CF40 2EL'
    #     # 'LLANHARRY COMMUNITY CENTRE, TYLACOCH, LLANHARRY, CF72 9LF'
    #     # 'TALBOT GREEN PAVILION, LANELAY ROAD, TALBOT GREEN, PONTYCLUN, CF72 8HY'
    #     # 'LLANHARAN RUGBY CLUB, BRIDGEND ROAD, LLANHARAN, PONTYCLUN, CF72 9RD'
    #     # 'COLEG Y CYMOEDD NANTGARW CAMPUS, RAIL BUILDING, GROUND FLOOR, PARC NANTGARW, HEOL Y COLEG, CARDIFF, CF15 7QY'
    #     # 'CARADOG PRIMARY SCHOOL, ACCESS VIA PENDARREN STREET, ABERDARE, CF44 7PE'
    #     # 'HOPE CHURCH RHONDDA, DUNRAVEN STREET, TONYPANDY, CF40 1AN'
    #     # 'THE FEEL GOOD FACTORY, ABERCYNON ROAD, YNYSYBOETH, MOUNTAIN ASH, CF45 4XZ'
    #     # 'COEDELY COMMUNITY CENTRE, ELY VALLEY ROAD, COEDELY, TONYREFAIL, CF39 8BL'
    #     # 'CYLCH MEITHRIN ABERDAR, WIND STREET, ABERDARE, CF44 7ES'

    #     return super().station_record_to_dict(record)

    # def address_record_to_dict(self, record):
    #     uprn = record.uprn.strip().lstrip("0")

    #     if (
    #         uprn
    #         in [
    #             "10090841724",  # THE STABLES MILL STREET, PONTYPRIDD
    #             "10024274643",  # 15 CLIFF TERRACE, TREFOREST, PONTYPRIDD
    #             "10094101639",  # 30 ILAN AVENUE, PONTYPRIDD
    #             "10094101649",  # 40 ILAN AVENUE, PONTYPRIDD
    #             "10001300469",  # 34 CAPEL FARM, TONYREFAIL, PORTH
    #             "200001640536",  # SAWMILLS HOUSE, LLANTRISANT, PONTYCLUN
    #             "10012770573",  # THE CROFT, LLANTRISANT, PONTYCLUN
    #             "10090596281",  # THE OLD LAMB & FLAG, LLANTRISANT, PONTYCLUN
    #             "10090596664",  # FARMHOUSE CASTELLAU FARM ROAD TO CASTELLAU FAWR FARM, CASTELLAU, BEDDAU
    #             "200003777546",  # SIGNALMANS COTTAGE, ELY VALLEY ROAD, YNYSMAERDY, PONTYCLUN
    #             "10090596707",  # FARMHOUSE FFORCH ORKY FARM CEMETERY ROAD, TREORCHY
    #         ]
    #     ):
    #         return None

    #     if record.housepostcode in [
    #         # splits
    #         "CF44 0PD",
    #         "CF38 1DR",
    #         "CF37 3BS",
    #         "CF42 6BH",
    #         "CF44 9TB",
    #         "CF39 8FA",
    #         "CF40 2ER",
    #         "CF37 1UA",
    #         "CF37 2HL",
    #         "CF37 4DX",
    #         "CF39 8AT",
    #         "CF38 2JZ",
    #         "CF44 9DT",
    #         "CF44 8LW",
    #         # looks wrong
    #         "CF37 4BP",
    #         "CF37 1PS",
    #     ]:
    #         return None

    #     return super().address_record_to_dict(record)
