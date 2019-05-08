from data_collection.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "E07000009"
    addresses_name = "local.2019-05-02/Version 1/Democracy Club - Polling Districts.csv"
    stations_name = "local.2019-05-02/Version 1/Democracy Club - Polling Stations.csv"
    elections = ["local.2019-05-02", "europarl.2019-05-23"]

    def station_record_to_dict(self, record):

        if record.stationcode == "MB1":
            # BRINKLEY MEMORIAL HALL
            record = record._replace(postcode="CB8 0SF")

        if record.stationcode == "LE1":
            # KENNETT PAVILION
            record = record._replace(postcode="CB8 7QF")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.uprn.strip().lstrip("0")

        if uprn == "10002600979":
            return None

        if uprn in [
            "100090044659"  # CB75EU -> CB61AJ : 14 FAIR FIELD CLOSE, SOHAM, CAMBRIDGESHIRE
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "10002591793",  # CB62DS -> CB62BU : HALE FEN HOUSE, 1 HALE FEN LANE, WARDY HILL, ELY
            "100091191582",  # CB80TS -> CB80UU : 2 GATEHOUSE COTTAGES, LOWER HARE PARK, LONDON ROAD, STETCHWORTH, NEWMARKET
        ]:
            rec["accept_suggestion"] = False

        return rec
