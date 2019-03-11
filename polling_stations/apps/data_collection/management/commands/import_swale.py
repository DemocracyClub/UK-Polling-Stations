from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "E07000113"
    addresses_name = (
        "local.2019-05-02/Version 1/polling_station_export-2019-02-28Swle.csv"
    )
    stations_name = (
        "local.2019-05-02/Version 1/polling_station_export-2019-02-28Swle.csv"
    )
    elections = ["local.2019-05-02"]

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
            "10035061220",  # ME121AG -> ME122AG : 178 Invicta Road, Sheerness, Kent
            "10093083738",  # ME124JB -> ME101QA : Flat Above Marinos Fish Bar 212 London Road, Sittingbourne, Kent
            "100061078990",  # ME123PA -> ME123NZ : 382B Minster Road, Minster-on-Sea, Sheerness, Kent
            "100061083074",  # ME122SG -> ME122SD : Llamedos The Glen, Minster-on-Sea, Sheerness, Kent
            "100062379223",  # ME124JA -> ME124JB : Sheringham Bell Farm Lane, Minster-on-Sea, Sheerness, Kent
            "100061073637",  # ME124JA -> ME124JB : The Laurels Bell Farm Lane, Minster-on-Sea, Sheerness, Kent
            "100061073623",  # ME124JA -> ME124JB : Merry Moments Bell Farm Lane, Minster-on-Sea, Sheerness, Kent
            "200002539987",  # ME101NL -> ME101NS : Flat L 94 London Road, Sittingbourne, Kent
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "100062087806",  # ME121TP -> ME122RT : Flat 2 36A Broadway, Sheerness, Kent
            "100062087803",  # ME121TP -> ME122RT : Flat 1 36A Broadway, Sheerness, Kent
            "200002535746",  # ME121NX -> ME102RD : 45A High Street, Sheerness, Kent
            "10013741961",  # ME130SG -> ME104ES : Winterbourne Cottage Annexe Rushett Lane, Norton, Faversham, Kent
            "10023196555",  # ME122DH -> ME121AG : 3 The Crescent Parklands Village The Broadway, Minster-on-Sea, Sheerness, Kent
            "10023196556",  # ME122DH -> ME121AG : 1 The Crescent Parklands Village The Broadway, Minster-on-Sea, Sheerness, Kent
            "10023200723",  # ME137JG -> ME98XF : 23 West Street, Faversham, Kent
        ]:
            rec["accept_suggestion"] = False

        return rec

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)

        if record.pollingstationnumber in ["113", "114"]:
            rec["location"] = Point(0.735912, 51.337309, srid=4326)

        return rec
