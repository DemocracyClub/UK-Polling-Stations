from data_collection.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "E07000095"
    addresses_name = (
        "parl.2019-12-12/Version 1/Democracy club - polling districts 12-12-2019.csv"
    )
    stations_name = (
        "parl.2019-12-12/Version 1/Democracy club - polling stations 12-12-2019.csv"
    )
    elections = ["parl.2019-12-12"]
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):

        # Fairfields primary school
        if record.stationcode in ["AHC_1", "AHE_1"]:
            record = record._replace(xordinate="534213")
            record = record._replace(yordinate="203580")

        # Flamstead End Hall
        if record.stationcode in ["AHD_1", "AHB_1", "AHA_1"]:
            record = record._replace(xordinate="535062")
            record = record._replace(yordinate="203335")

        # Fairley Cross Hall, Rosedale Community Church
        if record.stationcode in ["AJA_1", "AJC_1", "AJD_1"]:
            record = record._replace(xordinate="534455")
            record = record._replace(yordinate="203051")

        # These stations are outside the council area and don't appear in the addresses file
        if record.stationcode in ["DCB_1", "DCB_2", "DCC_1"]:
            return None

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.uprn.strip().lstrip("0")

        if uprn in ["148023093", "148022559"]:
            return None

        if uprn in [
            "148036797",  # EN89DG -> EN89DQ : 3 LEIGHTON COURT, TURNERS HILL, CHESHUNT, HERTFORDSHIRE
            "148048401",  # EN88JJ -> EN88EB : 4A THEOBALDS COURT, CROSSBROOK STREET, CHESHUNT, HERTFORDSHIRE
            "148004180",  # EN80JB -> EN80HT : 28 FLAMSTEAD END ROAD, CHESHUNT, HERTFORDSHIRE
            "148004473",  # EN107QQ -> EN107FF : HILL CROSS FARM, HOLY CROSS HILL, WORMLEY, HERTFORDSHIRE
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "148048304",  # EN88JJ -> EN118JJ : 3 ST GEORGES HOUSE, 100 CROSSBROOK STREET, CHESHUNT, HERTFORDSHIRE
            "148046488",  # EN106JJ -> EN106HT : 55A HIGH ROAD, WORMLEY, HERTFORDSHIRE
        ]:
            rec["accept_suggestion"] = False

        return rec
