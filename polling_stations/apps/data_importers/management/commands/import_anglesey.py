from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "AGY"
    addresses_name = "2024-05-02/2024-03-05T14:11:42.668428/Eros_SQL_Output001.csv"
    stations_name = "2024-05-02/2024-03-05T14:11:42.668428/Eros_SQL_Output001.csv"
    elections = ["2024-05-02"]

    def station_record_to_dict(self, record):
        # NEUADD BENTREF LLANFACHRAETH, LLANFACHRAETH, YNYS MON LL65 2UH
        if record.pollingstationnumber == "21":
            # confirming postcode
            record = record._replace(pollingstationpostcode="LL65 4UH")

        # YSGOLDY CAPEL M C CARMEL, CARMEL, YNYS MON LL71 8DA
        if record.pollingstationnumber == "20":
            # confirming postcode
            record = record._replace(pollingstationpostcode="LL71 7DH")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            # split
            "LL74 8ST",
            "LL65 2EL",
            "LL77 7NW",
        ]:
            return None

        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "200002649098",  # 4 TREMWYLFA, CARMEL, LLANNERCH-Y-MEDD
            "10024357287",  # CHAPEL HOUSE, SOUTH STACK ROAD, HOLYHEAD
            "10024356434",  # HENLLYS, LLANGAFFO, GAERWEN
            "10024359360",  # CAE'R WENNOL, LLANGAFFO, GAERWEN
            "10013463367",  # HARBOUR HOUSE, TRAETH BYCHAN, MARIANGLAS
            "10013466388",  # OLD GRANARY, PENTRAETH
            "10013853106",  # PANT Y BWLCH, LLANDDONA, BEAUMARIS
            "10013457915",  # CASTELL GRUG, SOUTH STACK, HOLYHEAD
        ]:
            return None
        return super().address_record_to_dict(record)
