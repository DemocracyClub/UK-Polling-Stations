from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "POW"
    addresses_name = "2024-07-04/2024-06-12T15:13:10.440907/Eros_SQL_Output004.csv"
    stations_name = "2024-07-04/2024-06-12T15:13:10.440907/Eros_SQL_Output004.csv"
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        if record.uprn in [
            "10011806077",  # COACH HOUSE, LLANBEDR ROAD, CRICKHOWELL
            "10011744832",  # RECTORY COTTAGE, CATHEDINE, BRECON
            "10011738931",  # ORCHARD COTTAGE, BRYNWERN HALL, LLANFIHANGEL BRYNPABUAN, BUILTH WELLS
            "10011741058",  # THE BRYN, OLD RADNOR, PRESTEIGNE
            "10011755050",  # COED COCHIAN, RHAYADER
            "10011797348",  # TY ISAF GLYNGYNWYDD A470T FROM LLANGURIG ROUNDABOUT TO JUNCTION WITH B4518 BY LLANIDLOES, LLANGURIG, LLANIDLOES
            "10011784973",  # HIGH OAK, DOLFOR ROAD, NEWTOWN
            "10011743355",  # TY MAWR C2091 FROM JUNCTION WITH C2001 STATION ROAD TO JUNCTION WITH PRIVATE TRACK LEADING TO TY MAWR, PEN-Y-BONT-FAWR, OSWESTRY
            "10011741376",  # THE SPRIGGS, CASCOB, PRESTEIGNE
        ]:
            return None

        if record.housepostcode in [
            # split
            "SY20 9NL",
            "SY22 6DE",
            "LD1 6TY",
            "LD3 0HG",
            "HR3 5JY",
            "LD3 9EF",
            "SY21 9AP",
            "SY21 0NG",
            "LD3 7HN",
            "SY21 0DT",
            "LD1 6UT",
            "SY16 3DW",
            "SY16 3DR",
            "SY17 5SA",
            "SY10 0LH",
            "SY21 7QU",
            "SY18 6NR",
            "SY16 1HG",
            "LD2 3UD",
            "SY22 6JG",
            "LD1 6SW",
            "SY18 6JD",
            "SY17 5PA",
            "SY18 6QT",
            "SY21 9AY",
            "SY21 9HZ",
            "SY20 8EX",
        ]:
            return None

        return super().address_record_to_dict(record)
