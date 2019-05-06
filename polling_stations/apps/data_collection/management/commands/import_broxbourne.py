from data_collection.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "E07000095"
    addresses_name = "local.2019-05-02/Version 1/Democracy club- polling districts for Borough of Broxbourne.csv"
    stations_name = "local.2019-05-02/Version 1/Democracy club- polling stations for Borough of Broxbourne.csv"
    elections = ["europarl.2019-05-23"]

    def station_record_to_dict(self, record):

        # user issue report #46
        if record.stationcode == "AHC_1":
            record = record._replace(xordinate="0")
            record = record._replace(yordinate="0")

        # station change for EU Parl elections
        if record.stationcode == "ACA_1":
            record = record._replace(add1="The Spinning Wheel")
            record = record._replace(add2="30 High Street")
            record = record._replace(add3="Hoddesdon")
            record = record._replace(add4="")
            record = record._replace(add5="")
            record = record._replace(add6="")
            record = record._replace(postcode="EN11 8BP")
            record = record._replace(xordinate="0")
            record = record._replace(yordinate="0")
            record = record._replace(placename="")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.uprn.strip().lstrip("0")

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
