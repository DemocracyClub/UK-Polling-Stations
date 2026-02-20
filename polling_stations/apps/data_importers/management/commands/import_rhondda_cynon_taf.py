from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "RCT"
    addresses_name = "2026-05-07/2026-02-23T12:49:15.549495/RCT_combined.csv"
    stations_name = "2026-05-07/2026-02-23T12:49:15.549495/RCT_combined.csv"
    elections = ["2026-05-07"]

    def station_record_to_dict(self, record):
        # postcode correction for: CILFYNYDD AND NORTON BRIDGE COMMUNITY CENTRE, CILFYNYDD ROAD, CILFYNYDD, PONTYPRIDD, CF37 3NR
        if (
            self.get_station_hash(record)
            == "46-cilfynydd-and-norton-bridge-community-centre"
        ):
            record = record._replace(pollingstationpostcode="CF37 4NR")

        # postcode correction for: ST LUKES CHURCH, CARDIFF ROAD, HAWTHORN, PONTYPRIDD, CF37 5LG
        if self.get_station_hash(record) == "63-st-lukes-church":
            record = record._replace(pollingstationpostcode="CF37 5LN")

        # adding postcode for: RHYDYFELIN LIBRARY, POPLAR ROAD, RHYDYFELIN, PONTYPRIDD
        if self.get_station_hash(record) == "61-rhydyfelin-library":
            record = record._replace(pollingstationpostcode="CF37 5LR")

        # The following stations postcodes have been confirmed with the council:

        # 'LLWYNYPIA BOYS AND GIRLS CLUB, LLWYNYPIA ROAD, TONYPANDY, CF40 2EL'
        # 'LLANHARRY COMMUNITY CENTRE, TYLACOCH, LLANHARRY, CF72 9LF'
        # 'TALBOT GREEN PAVILION, LANELAY ROAD, TALBOT GREEN, PONTYCLUN, CF72 8HY'
        # 'LLANHARAN RUGBY CLUB, BRIDGEND ROAD, LLANHARAN, PONTYCLUN, CF72 9RD'
        # 'COLEG Y CYMOEDD NANTGARW CAMPUS, RAIL BUILDING, GROUND FLOOR, PARC NANTGARW, HEOL Y COLEG, CARDIFF, CF15 7QY'
        # 'CARADOG PRIMARY SCHOOL, ACCESS VIA PENDARREN STREET, ABERDARE, CF44 7PE'
        # 'HOPE CHURCH RHONDDA, DUNRAVEN STREET, TONYPANDY, CF40 1AN'
        # 'THE FEEL GOOD FACTORY, ABERCYNON ROAD, YNYSYBOETH, MOUNTAIN ASH, CF45 4XZ'
        # 'COEDELY COMMUNITY CENTRE, ELY VALLEY ROAD, COEDELY, TONYREFAIL, CF39 8BL'
        # 'CYLCH MEITHRIN ABERDAR, WIND STREET, ABERDARE, CF44 7ES'

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10001300469",  # 34 CAPEL FARM, TONYREFAIL, PORTH
            "200003777546",  # SIGNALMANS COTTAGE, ELY VALLEY ROAD, YNYSMAERDY, PONTYCLUN
            "200002935304",  # POBL LIVING, 11-11A MILL STREET, PONTYPRIDD
        ]:
            return None

        if record.postcode in [
            # splits
            "CF44 0PD",
            "CF38 1DR",
            "CF37 3BS",
            "CF39 8GD",
            "CF40 2ER",
            "CF39 8FA",
            "CF39 8AT",
            "CF44 8LW",
            "CF44 9DT",
            # looks wrong
            "CF37 4BP",
            "CF37 1PS",
        ]:
            return None

        return super().address_record_to_dict(record)
