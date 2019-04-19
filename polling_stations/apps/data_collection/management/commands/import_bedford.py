from data_collection.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "E06000055"
    addresses_name = "local.2019-05-02/Version 1/Democracy Club polling districts.csv"
    stations_name = "local.2019-05-02/Version 1/Democracy Club Polling Stations.csv"
    elections = ["local.2019-05-02"]

    def station_record_to_dict(self, record):
        if record.stationcode == "BAS_1":
            record = record._replace(xordinate="0")
            record = record._replace(yordinate="0")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10093204769",  # MK401PE -> MK402SY : FLAT 10, HARPUR APARTMENTS, HARPUR STREET
            "100080999032",  # PE280ND -> PE280NE : NELSON COTTAGE, HIGH STREET, UPPER DEAN, Huntingdon
            "100080999044",  # PE280ND -> PE280NE : THE SPINNEY, HIGH STREET, UPPER DEAN, Huntingdon
            "10033178065",  # PE280NF -> PE280NE : DEAN LODGE, BROOK LANE, UPPER DEAN, Huntingdon
            "10024229957",  # MK442EY -> MK442EL : SKYLARKS, KIMBOLTON ROAD, BOLNHURST, BEDFORD
            "100081212998",  # MK442BZ -> MK442LD : BERRY WOOD FARM, LITTLE STAUGHTON ROAD, COLMWORTH, BEDFORD
        ]:
            rec["accept_suggestion"] = True

        return rec
