from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "POW"
    addresses_name = (
        "2024-05-02/2024-02-22T15:03:42.143260/Democracy Club - County of Powys.csv"
    )
    stations_name = (
        "2024-05-02/2024-02-22T15:03:42.143260/Democracy Club - County of Powys.csv"
    )
    elections = ["2024-05-02"]

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
        ]:
            return None

        if record.housepostcode in [
            # split
            "LD1 6UT",
            "HR3 5JY",
            "LD1 6TY",
            "SY5 9BT",
            "SY18 6JD",
            "LD3 0HG",
            "SY10 0LH",
            "LD3 9EF",
            "SY16 3DW",
            "SY21 7QU",
            "SY21 9AP",
            "SY16 1HG",
            "SY20 8EX",
            "LD3 7HN",
            "SY18 6QT",
            "LD2 3UD",
            "SY16 3DR",
            "SY17 5SA",
            "SY21 0DT",
            "SY21 0NG",
            "SY22 6JG",
            "SY18 6NR",
            "SY22 6DE",
            "SY17 5PA",
            "LD1 6SW",
            "SY21 9AY",
            "SY20 9NL",
            "SY21 9HZ",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Station changes  requested by council:
        # OLD: BRECON PRIORY SCHOOL PENDRE - N0.1 STATION, Priory C in W School, BRECON, LD3 9EU
        # NEW: BRECON ST JOHN'S CENTRE - Station No. 1, BRECON
        if record.pollingstationnumber == "34":
            record = record._replace(
                pollingstationname="BRECON ST JOHN'S CENTRE - Station No. 1",
                pollingstationaddress_1="",
                pollingstationaddress_2="",
                pollingstationaddress_3="",
                pollingstationaddress_4="",
                pollingstationpostcode="",
            )

        # OLD: BRECON PRIORY SCHOOL PENDRE - N0.2 STATION, Priory C in W School, BRECON, LD3 9EU
        # NEW: BRECON ST JOHN'S CENTRE - Station No. 2, BRECON
        if record.pollingstationnumber == "35":
            record = record._replace(
                pollingstationname="BRECON ST JOHN'S CENTRE - Station No. 2",
                pollingstationaddress_1="",
                pollingstationaddress_2="",
                pollingstationaddress_3="",
                pollingstationaddress_4="",
                pollingstationpostcode="",
            )

        # OLD: NEWTOWN EVANGELICAL CHURCH - STATION NO. 1, Newtown Evangelical Church, Llanidloes Road, NEWTOWN, SY16 1HL
        # NEW: NEWTOWN MALDWYN LEISURE CENTRE - STATION 1
        if record.pollingstationnumber == "155":
            record = record._replace(
                pollingstationname="NEWTOWN MALDWYN LEISURE CENTRE - STATION 1",
                pollingstationaddress_1="",
                pollingstationaddress_2="",
                pollingstationaddress_3="",
                pollingstationaddress_4="",
                pollingstationpostcode="",
            )

        # OLD: NEWTOWN EVANGELICAL CHURCH - STATION NO. 2, Newtown Evangelical Church, Llanidloes Road, NEWTOWN, SY16 1HL
        # NEW: NEWTOWN MALDWYN LEISURE CENTRE - STATION 2
        if record.pollingstationnumber == "157":
            record = record._replace(
                pollingstationname="NEWTOWN MALDWYN LEISURE CENTRE - STATION 2",
                pollingstationaddress_1="",
                pollingstationaddress_2="",
                pollingstationaddress_3="",
                pollingstationaddress_4="",
                pollingstationpostcode="",
            )

        return super().station_record_to_dict(record)
