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
