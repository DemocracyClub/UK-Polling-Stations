from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E09000032"
    addresses_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019wand.tsv"
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019wand.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):
        # St Andrew`s United Reformed Church
        if record.polling_place_id == "7252":
            record = record._replace(polling_place_postcode="SW12 9QH")

        # St John's Hill Residents Centre
        if record.polling_place_id == "7282":

            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-0.1699533, 51.4622247, srid=4326)
            return rec

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in ["10094189386", "10008155689", "10070240542"]:
            return None

        if uprn == "121040397":
            rec["postcode"] = "SW179NN"
            rec["accept_suggestion"] = False

        if uprn in [
            "121048817",  # SW129BE -> SW129BA : Flat 1, 189 Balham High Road, London
            "121048818",  # SW129BE -> SW129BA : Flat 2, 189 Balham High Road, London
            "121048819",  # SW129BE -> SW129BA : Flat 3, 189 Balham High Road, London
            "121028687",  # SW155PJ -> SW115PJ : 29 Lawrence Froebel College, Roehampton Lane, London
            "100022668375",  # SW111BL -> SW113GZ : 103A Mallinson Road, London
            "100022613599",  # SW111BL -> SW113GZ : 103C Mallinson Road, London
            "121026201",  # SW111BH -> SW113GX : First Floor Flat, 125 Mallinson Road, London
            "10024086170",  # SW154JL -> SW154JD : Huntercombe Hospital, Holybourne Avenue, London
            "121049779",  # SW156TH -> SW152TH : 282A Upper Richmond Road, London
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "10008156178",  # SW177BB -> SW179BU : A302 A Block, Furzedown Education Site, Spalding Road, London
            "10093416547",  # SW114ND -> SW179PU : Flat A, 146 Battersea Park Road, London
            "10093416548",  # SW114ND -> SW179PU : Flat B, 146 Battersea Park Road, London
            "10093416549",  # SW114ND -> SW179PU : Flat C, 146 Battersea Park Road, London
            "121051059",  # SW182SL -> SW111PA : Flat B, 50 North Side Wandsworth Common, London
            "10091503361",  # SW151SS -> SW152PA : 97B Putney High Street, London
        ]:
            rec["accept_suggestion"] = False

        return rec
