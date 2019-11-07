from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "E07000113"
    addresses_name = (
        "parl.2019-12-12/Version 1/polling_station_export-2019-11-04swale.csv"
    )
    stations_name = (
        "parl.2019-12-12/Version 1/polling_station_export-2019-11-04swale.csv"
    )
    elections = ["parl.2019-12-12"]
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "200001875126",  # ME122HP -> ME122LZ : Morland House Augustine Road, Minster-on-Sea, Sheerness, Kent
            "100061078702",  # ME122LE -> ME122LA : Uppal Villa Minster Drive, Minster-on-Sea, Sheerness, Kent
            "100061081138",  # ME122LS -> ME122LX : 150 Scarborough Drive, Minster-on-Sea, Sheerness, Kent
            "10023197317",  # ME122SG -> ME122SH : 1A Baldwin Cottage Baldwin Road, Minster-on-Sea, Sheerness, Kent
            "10023197934",  # ME122LT -> ME122LX : 152 Scarborough Drive, Minster-on-Sea, Sheerness, Kent
            "100061080835",  # ME123JE -> ME123HT : 1A Rosemary Avenue, Minster-on-Sea, Sheerness, Kent
            "10023200030",  # ME103TU -> ME123TU : 28 Petunia Avenue, Minster-on-Sea, Sheerness, Kent
            "100061083074",  # ME122SG -> ME122SD : Llamedos The Glen, Minster-on-Sea, Sheerness, Kent
            "200002539987",  # ME101NL -> ME101NS : Flat L 94 London Road, Sittingbourne, Kent
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "100062087806",  # ME121TP -> ME122RT : Flat 2 36A Broadway, Sheerness, Kent
            "100062087803",  # ME121TP -> ME122RT : Flat 1 36A Broadway, Sheerness, Kent
            "10023196555",  # ME122DH -> ME121AG : 3 The Crescent Parklands Village The Broadway, Minster-on-Sea, Sheerness, Kent
        ]:
            rec["accept_suggestion"] = False

        return rec
