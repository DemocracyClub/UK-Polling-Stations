from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "AGY"
    addresses_name = "2024-07-04/2024-06-18T10:03:58.926929/Eros_SQL_Output003.csv"
    stations_name = "2024-07-04/2024-06-18T10:03:58.926929/Eros_SQL_Output003.csv"
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            # split
            "LL74 8ST",
            "LL65 2EL",
            "LL77 7NW",
            # suspect
            "LL77 7UR",
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
            "10013466115",  # RHANDIR, LLANFIGAEL, HOLYHEAD
            "10013463941",  # TYN DRYFOL BACH, BODORGAN
            "10013457915",  # CASTELL GRUG, SOUTH STACK, HOLYHEAD
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # YR HEN FECWS, DWYRAN, YNYS MON
        if self.get_station_hash == "62-yr-hen-fecws":
            record = record._replace(pollingstationpostcode="LL61 6AU")
        # NEUADD EGLWYS SANTES FAIR, 1 FFORDD BRYNGWYN, CAERGYBI, YNYS MON
        if self.get_station_hash(record) == "7-neuadd-eglwys-santes-fair":
            record = record._replace(pollingstationpostcode="LL65 1TR")
        # NEUADD GYMUNED LLAINGOCH, SOUTH STACK ROAD, LLAINGOCH, CAERGYBI / HOLYHEAD, YNYS MON
        if self.get_station_hash(record) == "5-neuadd-gymuned-llaingoch":
            record = record._replace(pollingstationpostcode="LL65 1LU")
        return super().station_record_to_dict(record)
