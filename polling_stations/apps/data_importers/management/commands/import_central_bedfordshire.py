from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "CBF"
    addresses_name = "2024-07-04/2024-06-10T12:59:59.601292/districts-combined.csv"
    stations_name = "2024-07-04/2024-06-10T12:59:59.601292/stations-combined.csv"
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        if record.postcode in [
            "MK17 9QG",  # split
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        if record.stationcode in (
            # Stations with no addresses assigned
            "BX122M-BKMC",  # Elstow Playing Field Association Hall  (BDF)
            "BX123MD",  # Elstow Playing Field Association Hall  (BDF)
            "BX124MF-1",  # Lakeview Village Hall  (BDF)
            "BX125MF-2",  # Lakeview Village Hall  (BDF)
            "BX126ME/1",  # Stewartby Village Hall  (BDF)
            "BX127ME/2",  # Stewartby Village Hall  (BDF)
            "BX128MG",  # Wilstead Village Hall  (BDF)
            "BX129MH",  # Wilstead Village Hall  (BDF)
            "BX130MK-A",  # Wootton Community Centre  (BDF)
            "BX131MK-B",  # Wootton Community Centre  (BDF)
            "BX132ML",  # Wootton Memorial Hall  (BDF)
            "BX133MJ",  # Wootton Village Hall  (BDF)
        ):
            return None
        # bug report: removes wrong point for: Flitton Church Hall, Brook Lane, Flitton, Beds
        if record.stationcode == "BX55WF-G1":
            record = record._replace(xordinate="505929", yordinate="235815")
        return super().station_record_to_dict(record)
