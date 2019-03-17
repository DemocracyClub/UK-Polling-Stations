from data_collection.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "E07000095"
    addresses_name = "local.2019-05-02/Version 1/Democracy club- polling districts for Borough of Broxbourne.csv"
    stations_name = "local.2019-05-02/Version 1/Democracy club- polling stations for Borough of Broxbourne.csv"
    elections = ["local.2019-05-02"]

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
