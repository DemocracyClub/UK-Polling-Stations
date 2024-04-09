from addressbase.models import Address
from data_importers.management.commands import BaseHalaroseCsvImporter
from django.contrib.gis.geos import Point
from django.core.exceptions import ObjectDoesNotExist

WANBOROUGH_VILLAGE_HALL = {
    "pollingstationname": "Wanborough Village Hall",
    "pollingstationaddress_1": "Wanborough Hill",
    "pollingstationaddress_2": "Wanborough",
    "pollingstationaddress_3": "Guildford",
    "pollingvenueuprn": "10007084973",
    "pollingstationpostcode": "",
}


class Command(BaseHalaroseCsvImporter):
    council_id = "GRT"
    addresses_name = "2024-05-02/2024-02-28T11:16:15.797223/Eros_SQL_Output001.csv"
    stations_name = "2024-05-02/2024-02-28T11:16:15.797223/Eros_SQL_Output001.csv"
    elections = ["2024-05-02"]

    def station_record_to_dict(self, record):
        # Lancaster Hall, Send Road, Send, Woking GU23 6ET
        if self.get_station_hash(record) in [
            "41-lancaster-hall",
            "42-lancaster-hall",
        ]:
            record = record._replace(pollingstationpostcode="GU23 7ET")

        # Fix from council:
        # Old station: The Granary, Wanborough, Guildford GU3 2JR
        # New station: Wanborough Village Hall, Wanborough Hill, Wanborough, Guildford (uprn: 10007084973)
        if (record.pollingstationnumber, record.pollingstationname) == (
            "37",
            "The Granary",
        ):
            record = record._replace(**WANBOROUGH_VILLAGE_HALL)

            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-0.662221, 51.231466, srid=4326)

            return rec

        # coordinates from council:
        rec = super().station_record_to_dict(record)
        # Burpham Village Hall, Burpham Lane, Burpham, Guildford, GU4 7LP
        if rec["internal_council_id"] == "12-burpham-village-hall":
            rec["location"] = Point(501304.93, 152248.19, srid=27700)
            return rec

        # St. Mary's Church Community Centre, Vale Road, Ash Vale, Aldershot, GU12 5JE
        if rec["internal_council_id"] == "4-st-marys-church-community-centre":
            rec["location"] = Point(489265.7, 152505.65, srid=27700)
            return rec

        # The Benson Room, Japonica Court, Shawfield Road, Ash, Aldershot, GU12 6QU
        if rec["internal_council_id"] == "5-the-benson-room-japonica-court":
            rec["location"] = Point(488802.63, 150503.06, srid=27700)
            return rec

        # Ripley Village Hall (Victory House), High Street, Ripley, Woking, GU23 6AF
        if rec["internal_council_id"] == "40-ripley-village-hall-victory-house":
            rec["location"] = Point(505005.32, 156581.64, srid=27700)
            return rec

        # Chilworth Village Hall, New Road, Chilworth, Guildford, GU4 8LX
        if rec["internal_council_id"] == "46-chilworth-village-hall":
            rec["location"] = Point(502250, 147049, srid=27700)
            return rec

        # Lord Pirbright Hall, The Green, Pirbright, Woking, GU24 0JE
        if rec["internal_council_id"] == "28-lord-pirbright-hall":
            rec["location"] = Point(494578, 155985, srid=27700)
            return rec

        # King George V Hall, Browns Lane, Effingham, Leatherhead, KT24 5ND
        if rec["internal_council_id"] == "23-king-george-v-hall":
            rec["location"] = Point(511993, 153522, srid=27700)
            return rec

        # The Stirling Centre, St John's Church, Stoke Road, Guildford, GU1 1HB
        if rec["internal_council_id"] == "49-the-stirling-centre":
            rec["location"] = Point(499827, 150714, srid=27700)
            return rec

        # Bellfields Youth Centre, Hazel Avenue, Guildford, GU1 1NS
        if rec["internal_council_id"] == "9-bellfields-youth-centre":
            rec["location"] = Point(499163.78, 152257.58, srid=27700)
            return rec

        # First Jacobs Well Scout & Guide Group HQ, Jacobs Well Road, Guildford, GU4 7PD
        if rec["internal_council_id"] == "68-first-jacobs-well-scout-guide-group-hq":
            rec["location"] = Point(500051.94, 152983.88, srid=27700)
            return rec

        # Worplesdon Memorial Hall, Perry Hill, Worplesdon, Guildford, GU3 3RF
        if rec["internal_council_id"] == "67-worplesdon-memorial-hall":
            rec["location"] = Point(497031, 154002, srid=27700)
            return rec

        # Primrose Hall, Church View, Ash, Aldershot, GU12 6RX
        if rec["internal_council_id"] == "6-primrose-hall":
            rec["location"] = Point(489361.32, 150756.69, srid=27700)
            return rec

        # East Clandon Village Hall, The Street, East Clandon, Guildford, GU4 7RX
        if rec["internal_council_id"] == "13-east-clandon-village-hall":
            rec["location"] = Point(505997.58, 151694.52, srid=27700)
            return rec

        # St. Mark's Hall, Guildford Road, Normandy, Guildford, GU3 2DA
        if rec["internal_council_id"] == "27-st-marks-hall":
            rec["location"] = Point(492230.76, 151444.99, srid=27700)
            return rec

        # St. Clare's Church, Applegarth Avenue, Guildford, GU2 8LZ
        if rec["internal_council_id"] == "61-st-clares-church":
            rec["location"] = Point(497008, 150307, srid=27700)
            return rec

        # Emmanuel Parish Centre, Shepherds Lane, Stoughton, Guildford, GU2 9SJ
        if rec["internal_council_id"] == "53-emmanuel-parish-centre":
            rec["location"] = Point(498218, 151555, srid=27700)
            return rec

        # Sutherland Memorial Hall, Clay Lane, Burpham, Guildford, GU4 7JU
        if rec["internal_council_id"] == "11-sutherland-memorial-hall":
            rec["location"] = Point(501423, 152276, srid=27700)
            return rec

        # Emmanuel Parish Centre, Shepherds Lane, Stoughton, Guildford, GU2 9SJ
        if rec["internal_council_id"] == "52-emmanuel-parish-centre":
            rec["location"] = Point(498218, 151555, srid=27700)
            return rec

        # Peasmarsh Church Hall, Unstead Wood, Peasmarsh, Guildford, GU3 1ND
        if rec["internal_council_id"] == "44-peasmarsh-church-hall":
            rec["location"] = Point(499185, 146446, srid=27700)
            return rec

        # Chilworth Village Hall, New Road, Chilworth, Guildford, GU4 8LX
        if rec["internal_council_id"] == "56-chilworth-village-hall":
            rec["location"] = Point(502250, 147049, srid=27700)
            return rec

        # Albury Village Hall, The Street, Albury, Guildford, GU5 9AD
        if rec["internal_council_id"] == "57-albury-village-hall":
            rec["location"] = Point(505051, 147909, srid=27700)
            return rec

        # Compton Village Hall, The Street, Compton, Guildford, GU3 1EG
        if rec["internal_council_id"] == "43-compton-village-hall":
            rec["location"] = Point(495693.51, 146872.97, srid=27700)
            return rec

        # St. Martin's Church Hall (Canterbury Rooms), Ockham Road South, East Horsley, Leatherhead, KT24 6RL
        if rec["internal_council_id"] == "15-st-martins-church-hall-canterbury-rooms":
            rec["location"] = Point(509551, 152785, srid=27700)
            return rec

        # St. Joseph's Church Hall, Eastgate Gardens, Guildford, GU1 4AZ
        if rec["internal_council_id"] == "48-st-josephs-church-hall":
            rec["location"] = Point(500062, 149879, srid=27700)
            return rec

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "100062134282",  # FLAT 1 30 YORK ROAD, GUILDFORD
        ]:
            return None
        if record.housepostcode in [
            # split
            "GU1 4TJ",
            "GU23 7JL",
            "GU10 1BP",
            # suspect
            "GU5 9QN",
        ]:
            return None

        if (record.pollingstationnumber, record.pollingstationname) == (
            "37",
            "The Granary",
        ):
            record = record._replace(**WANBOROUGH_VILLAGE_HALL)

        return super().address_record_to_dict(record)

    # quick fix to show maps for Halarose records that have a valid UPRN in the PollingVenueUPRN field
    def get_station_point(self, record):
        uprn = record.pollingvenueuprn.strip().lstrip("0")
        try:
            ab_rec = Address.objects.get(uprn=uprn)
            return ab_rec.location
        except ObjectDoesNotExist:
            return None
