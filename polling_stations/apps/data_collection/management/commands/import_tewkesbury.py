from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000083"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019Tewk.tsv"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019Tewk.tsv"
    elections = ["europarl.2019-05-23"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):

        # one station change for EU election
        if record.polling_place_id == "7309":
            record = record._replace(polling_place_name="The Gambier Parry Hall")
            record = record._replace(polling_place_address_1="Highnam Community Centre")
            record = record._replace(polling_place_address_2="Newent Road")
            record = record._replace(polling_place_address_3="Glos")
            record = record._replace(polling_place_address_4="")
            record = record._replace(polling_place_postcode="GL2 8DG")
            record = record._replace(polling_place_easting="0")
            record = record._replace(polling_place_northing="0")
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-2.295441, 51.874659, srid=4326)
            return rec

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if record.post_code == "GL52 5QG":
            rec["postcode"] = "GL52 9QG"
            rec["accept_suggestion"] = False

        if uprn in ["200004320994", "200004330341"]:
            return None

        if uprn in [
            "10013762393",  # GL528SA -> GL528DQ : The Manor House, Cleeveway Manor, Evesham Road, Bishops Cleeve, Cheltenham, Glos
            "100121258121",  # GL29PQ -> GL29PU : The Cottage, Tewkesbury Road, Twigworth, Gloucester
            "200004335463",  # WR127ND -> WR127NE : Liberty Farm, Stanton, Broadway
            "200004330125",  # WR127NQ -> WR127ND : New House Farm, Stanton Road, Stanton, Broadway, Glos
            "10067629295",  # GL545PP -> GL545NY : 2 Millhampost Barn, Stanway, Cheltenham, Glos
            "10090023401",  # GL206JL -> GL208GN : 8 Styles Close, Northway, Tewkesbury, Glos
            "10093223390",  # GL208HQ -> GL208RY : The Coach House, Northway Court Farmhouse, Hardwick Bank Road, Northway, Tewkesbury, Glos
            "200004329486",  # GL510TL -> GL510TW : Brooklaines Farm, Barrow, Boddington, Cheltenham, Glos
            "200004331100",  # GL206JL -> GL206JD : The Granary, 1 Greenacres, Twyning, Tewkesbury, Glos
            "100121258576",  # GL205PR -> GL205PP : 2 Kings Head Cottages, Barton Street, Tewkesbury, Glos
            "100120547768",  # GL205PR -> GL205PP : 3 Kings Head Cottages, Barton Street, Tewkesbury, Glos
            "100120553601",  # GL545QP -> GL545AB : Langley Lodge, Langley Road, Winchcombe, Cheltenham, Glos
            "100120553581",  # GL545QP -> GL545AB : Cotmore, Langley Road, Winchcombe, Cheltenham, Glos
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "200004318039",  # GL28DQ -> GL528DH : Fairie Meade, 5 The Green, Highnam, Gloucester
            "10090020563",  # WR117TR -> WR117QN : 3 Raymeadow Cottages, Dumbleton, Evesham, Worcestershire
            "200004319980",  # GL29LS -> GL510TW : Church House, Church Lane, Norton, Gloucester
            "10067627280",  # GL205PP -> GL206DL : 2 Tysoes Court, 5A Barton Street, Tewkesbury, Glos
        ]:
            rec["accept_suggestion"] = False

        return rec
