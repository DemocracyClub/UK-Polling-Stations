from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "POW"
    addresses_name = "2026-05-07/2026-02-19T16:03:18.493604/POW_combined.csv"
    stations_name = "2026-05-07/2026-02-19T16:03:18.493604/POW_combined.csv"
    elections = ["2026-05-07"]

    def address_record_to_dict(self, record):
        if (
            record.uprn
            in [
                "10011806077",  # COACH HOUSE, LLANBEDR ROAD, CRICKHOWELL
                "10011744832",  # RECTORY COTTAGE, CATHEDINE, BRECON
                "10011741058",  # THE BRYN, OLD RADNOR, PRESTEIGNE
                "10011755050",  # COED COCHIAN, RHAYADER
                "10011797348",  # TY ISAF GLYNGYNWYDD A470T FROM LLANGURIG ROUNDABOUT TO JUNCTION WITH B4518 BY LLANIDLOES, LLANGURIG, LLANIDLOES
                "10011784973",  # HIGH OAK, DOLFOR ROAD, NEWTOWN
                "10011743355",  # TY MAWR C2091 FROM JUNCTION WITH C2001 STATION ROAD TO JUNCTION WITH PRIVATE TRACK LEADING TO TY MAWR, PEN-Y-BONT-FAWR, OSWESTRY
                "10011741376",  # THE SPRIGGS, CASCOB, PRESTEIGNE
            ]
        ):
            return None

        if record.postcode in [
            # split
            "SY18 6QT",
            "SY22 6DE",
            "SY17 5PA",
            "SY18 6NR",
            "LD3 0HG",
            "LD1 6SW",
            "SY16 3DR",
            "SY20 9NL",
            "SY16 3DW",
            "SY16 1HG",
            "HR3 5JY",
            "LD1 6TY",
            "LD3 9EF",
            "SY21 7QU",
            "SY20 8EX",
            "SY21 0NG",
            "SY21 9AP",
            "SY22 6JG",
            "SY18 6JD",
            "SY21 9HZ",
            "SY21 0DT",
            "SY21 9AY",
        ]:
            return None

        return super().address_record_to_dict(record)
