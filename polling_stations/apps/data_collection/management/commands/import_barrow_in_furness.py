from data_collection.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "E07000027"
    addresses_name = "parl.2019-12-12/Version 1/Democracy Club - Polling Districts.csv"
    stations_name = "parl.2019-12-12/Version 1/Democracy Club - Polling Stations.csv"
    elections = ["parl.2019-12-12"]
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "36016015",  # LA141DU -> LA145AY : 26 Crellin Street, Barrow-in-Furness
            "36025851",  # LA139HY -> LA139LT : 81 Newbarns Village, Hollow Lane, Barrow-in-Furness
            "36047048",  # LA130UF -> LA142UJ : 7 Rosewood Grove, Barrow-in-Furness
            "36030436",  # LA158BQ -> LA158BD : 43 Mount Pleasant, Skelgate, Dalton-in-Furness
            "36034298",  # LA130PD -> LA130PB : North Lodge, Abbey Road, Dalton-in-Furness
            "36031188",  # LA130NF -> LA130NX : The Bungalow, Greystone Lane, Dalton-in-Furness
            "36031184",  # LA130NF -> LA130ED : North Stank Farm, Newton Cross Road, Newton-in-Furness
            "36033063",  # LA158RP -> LA158HY : 40 Bankside, Broughton Road, Dalton-in-Furness
        ]:
            rec["accept_suggestion"] = False

        return rec

    def station_record_to_dict(self, record):

        if record.stationcode in ["LC/1", "LC/2"]:
            record = record._replace(xordinate="321436")
            record = record._replace(yordinate="477564")

        if record.stationcode == "AA/1":
            record = record._replace(xordinate="318608")
            record = record._replace(yordinate="468975")

        return super().station_record_to_dict(record)
