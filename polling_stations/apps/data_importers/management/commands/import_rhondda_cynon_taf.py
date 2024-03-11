from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "RCT"
    addresses_name = "2024-05-02/2024-03-11T10:56:12.180124/Eros_SQL_Output004.csv"
    stations_name = "2024-05-02/2024-03-11T10:56:12.180124/Eros_SQL_Output004.csv"
    elections = ["2024-05-02"]
    csv_encoding = "windows-1252"

    def station_record_to_dict(self, record):
        # postcode correction for: ST DAVIDS CHURCH, LLANTRISANT ROAD, GROESFAEN, PONTYCLUN, CF72 8NU
        if record.pollingstationnumber == "123":
            record = record._replace(pollingstationpostcode="CF72 8NS")

        # postcode correction for: CILFYNYDD AND NORTON BRIDGE COMMUNITY CENTRE, CILFYNYDD ROAD, CILFYNYDD, PONTYPRIDD, CF37 3NR
        if record.pollingstationnumber == "97":
            record = record._replace(pollingstationpostcode="CF37 4NR")

        # postcode correction for: ST LUKES CHURCH, CARDIFF ROAD, HAWTHORN, PONTYPRIDD, CF37 5LG
        if record.pollingstationnumber == "113":
            record = record._replace(pollingstationpostcode="CF37 5LN")

        # adding postcode for: RHYDYFELIN LIBRARY, POPLAR ROAD, RHYDYFELIN, PONTYPRIDD
        if record.pollingstationnumber == "111":
            record = record._replace(pollingstationpostcode="CF37 5LR")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10090841724",  # THE STABLES MILL STREET, PONTYPRIDD
            "10024274643",  # 15 CLIFF TERRACE, TREFOREST, PONTYPRIDD
            "10094101639",  # 30 ILAN AVENUE, PONTYPRIDD
            "10094101649",  # 40 ILAN AVENUE, PONTYPRIDD
            "10001300469",  # 34 CAPEL FARM, TONYREFAIL, PORTH
            "200001640536",  # SAWMILLS HOUSE, LLANTRISANT, PONTYCLUN
            "10012770573",  # THE CROFT, LLANTRISANT, PONTYCLUN
            "10090596281",  # THE OLD LAMB & FLAG, LLANTRISANT, PONTYCLUN
            "10090596664",  # FARMHOUSE CASTELLAU FARM ROAD TO CASTELLAU FAWR FARM, CASTELLAU, BEDDAU
            "200003777546",  # SIGNALMANS COTTAGE, ELY VALLEY ROAD, YNYSMAERDY, PONTYCLUN
            "10090596707",  # FARMHOUSE FFORCH ORKY FARM CEMETERY ROAD, TREORCHY
        ]:
            return None

        if record.housepostcode in [
            # splits
            "CF44 0PD",
            "CF38 1DR",
            "CF37 3BS",
            "CF42 6BH",
            "CF44 9TB",
            "CF39 8FA",
            "CF40 2ER",
            "CF37 1UA",
            "CF37 2HL",
            "CF37 4DX",
            "CF39 8AT",
            "CF38 2JZ",
            "CF44 9DT",
            # looks wrong
            "CF37 4BP",
            "CF37 1PS",
        ]:
            return None

        return super().address_record_to_dict(record)
