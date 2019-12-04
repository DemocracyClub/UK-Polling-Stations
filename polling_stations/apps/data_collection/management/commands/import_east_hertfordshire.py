from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000242"
    addresses_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019eh.tsv"
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019eh.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "10033104592":
            rec["postcode"] = "CM20 2QP"

        if uprn == "10023088041":
            rec["postcode"] = "CM20 2FP"

        if uprn in [
            "100080727137",  # CM233QY -> CM235QY : 34 Shortcroft, Bishops Stortford, Herts
            "100081117602",  # CM232JH -> CM232JJ : Wintersett, 5 Whitehall Lane, Bishops Stortford, Herts
            "10033104823",  # SG141LR -> SG142PX : Rose Cottage, Goldings Lane, Hertford, Herts
            "10034515290",  # CM210HX -> CM210DB : 36 Highfield, Crofters, Sawbridgeworth, Herts
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "100080722649",  # CM232QT -> CM232QY : 70 Hadham Road, Bishops Stortford, Herts
            "100081118102",  # SG90DX -> SG90DY : The Small Barn, Hare Street, Herts
            "100080736259",  # SG142LB -> SG142LG : The Hill, 236/238 Hertingfordbury Road, Hertford, Herts
            "10034620003",  # SG142NE -> SG142NA : The Lodge, Marden Hill, Hertford, Herts, Herts
            "100081121082",  # SG111PW -> SG111PJ : Tregarron, Standon Hill, Ware, Herts
            "10033095127",  # SG143NE -> SG143NQ : The Beehive Cottage, Woodhall Park, Watton At Stone, Herts
            "10033095128",  # SG143NE -> SG143NQ : The Garden House, Woodhall Park, Watton At Stone, Herts
            "100081120184",  # SG111NW -> SG111NY : Bromley Hall, Bromley Lane, Standon, Herts
        ]:
            rec["accept_suggestion"] = False

        return rec

    def station_record_to_dict(self, record):

        # Albury Village Hall
        if record.polling_place_id == "3349":
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(0.094440, 51.903865, srid=4326)
            return rec
        # Rhodes Arts Complex
        if record.polling_place_id == "3178":
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(0.163535, 51.863442, srid=4326)
            return rec

        return super().station_record_to_dict(record)
