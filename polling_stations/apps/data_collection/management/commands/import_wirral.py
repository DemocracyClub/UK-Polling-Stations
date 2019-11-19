from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E08000015"
    addresses_name = (
        "parl.2019-12-12/Version 1/Democracy_Club__12December2019Wirral.csv"
    )
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019Wirral.csv"
    elections = ["parl.2019-12-12"]
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):

        # Marlowe Road URC Hall
        if record.polling_place_id in ["5873"]:
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-3.050648, 53.417306, srid=4326)
            return rec

        # user issue report #87
        # The Grange Public House
        if record.polling_place_id == "5895":
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-3.122875, 53.396797, srid=4326)
            return rec

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "42194145":
            return None

        if uprn == "42191192":
            rec["postcode"] = "CH62 1AB"
            rec["accept_suggestion"] = False

        if (
            record.addressline1.strip() == "136 Wallasey Road"
            and record.addressline2.strip() == "Wallasey"
            and record.addressline3.strip() == "Wirral"
        ):
            rec["postcode"] = "CH44 2AF"

        if uprn in [
            "42072401",  # CH434TS -> CH431TS : 29 Mather Road, Oxton, Wirral
            "42072402",  # CH434TS -> CH431TS : 29A Mather Road, Oxton, Wirral
            "42072403",  # CH434TS -> CH431TS : 29B Mather Road, Oxton, Wirral
            "42081451",  # CH439TT -> CH439UE : Wexford Ridge, Noctorum Lane, Oxton, Wirral
            "42181578",  # CH474AU -> CH472DH : 10 Market Street, Hoylake, Wirral
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "42092437",  # CH427LQ -> CH427LG : 5 Prenton Road East, Higher Tranmere, Wirral
            "42168891",  # CH414DB -> CH414DP : Flat 1, 70 Grange Road West, Claughton, Wirral
            "42168892",  # CH414DB -> CH414DP : Flat 2, 70 Grange Road West, Claughton, Wirral
            "42080139",  # CH628AB -> CH628BP : Plymyard Lodge, New Chester Road, Bromborough, Wirral
            "42156413",  # CH421PU -> CH421PP : Flat 1 Summer Hill, The Dell, Rock Ferry, Wirral
            "42156414",  # CH421PU -> CH421PP : Flat 2 Summer Hill, The Dell, Rock Ferry, Wirral
            "42156415",  # CH421PU -> CH421PP : Flat 3 Summer Hill, The Dell, Rock Ferry, Wirral
            "42156416",  # CH421PU -> CH421PP : Flat 4 Summer Hill, The Dell, Rock Ferry, Wirral
            "42166053",  # CH494LR -> CH494NN : 36A Overchurch Road, Upton, Wirral
            "42085274",  # CH494LR -> CH494NN : 36 Overchurch Road, Upton, Wirral
            "42005952",  # CH431US -> CH435RE : Flat 1, 56 Balls Road, Oxton, Wirral
            "42005953",  # CH431US -> CH435RE : Flat 2, 56 Balls Road, Oxton, Wirral
            "42005954",  # CH431US -> CH435RE : Flat 3, 56 Balls Road, Oxton, Wirral
            "42000172",  # CH447BH -> CH484DD : 1 Acacia Grove, Wallasey, Wirral
            "42181259",  # CH426PU -> CH625BQ : Flat, 30 Bebington Road, Higher Tranmere, Wirral
            "42016382",  # CH636JA -> CH636HY : Home Farm, Brimstage Lane, Brimstage, Wirral
            "42166160",  # CH630NN -> CH630NB : 1 Raby Hall Farm Cottage, Raby Hall Road, Raby, Wirral
            "42189392",  # CH431TE -> CH431SZ : Grove House, 1 Palm Grove, Claughton, Wirral
            "42120863",  # CH437PN -> CH437PT : Beverley, 39 Vyner Road South, Prenton, Wirral
            "42132798",  # CH616UZ -> CH616UY : 75 Irby Road, Heswall, Wirral
            "42119402",  # CH472AN -> CH472AW : 21A Valentia Road, Hoylake, Wirral
            "42118874",  # CH496LN -> CH496LP : Cherie Field, Upland Road, Upton, Wirral
        ]:
            rec["accept_suggestion"] = False

        return rec
