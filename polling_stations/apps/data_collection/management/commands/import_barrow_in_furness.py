from data_collection.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "E07000027"
    addresses_name = "local.2019-05-02/Version 1/DemocracyClubPollingDistrictsbdc.csv"
    stations_name = "local.2019-05-02/Version 1/DemocracyClubPollingStationsbdc.csv"
    elections = ["local.2019-05-02"]

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "36025885"  # LA130PJ -> LA130PG : West Gate Cottage, Manor Road, Barrow-in-Furness
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "36015231",  # LA141BS -> LA141DU : 289 Rawlinson Street, Barrow-in-Furness
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
