from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000214"
    addresses_name = (
        "parl.2019-12-12/Version 2/Express Property UPRN and polling station number.txt"
    )
    stations_name = (
        "parl.2019-12-12/Version 2/Express Property UPRN and polling station number.txt"
    )
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):
        if (
            record.polling_place_id == "2528"
            and record.polling_place_postcode == "GU20 6HJ"
        ):
            # Chertsey Road Hall,  41 Chertsey Road
            record = record._replace(polling_place_postcode="GU20 6EW")
        rec = super().station_record_to_dict(record)

        # From: 972106:polling_stations/apps/data_collection/management/commands/misc_fixes.py-245-
        if rec["internal_council_id"] == "2503":  # Heatherside Community Centre
            rec["location"] = Point(-0.702364, 51.329003, srid=4326)

        return rec

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if "Lucas Drive" in record.addressline1:
            rec["postcode"] = "GU249JQ"

        if uprn == "200000199948":  # Medcote Cottage, Water Lane
            return None

        if uprn == "10002681200":
            # Split postcode anyway, and this one has an unexpected polling station ID, so play it safe.
            return None

        if record.post_code == "GU206LJ":
            # Split postcode with weird distribution
            return None

        if uprn in [
            "100061567393",  # GU195ES -> GU249PJ : 37 Oakridge, West End, Woking, Surrey
            "100062330131",  # GU166NS -> GU166HY : The Bungalow, Frimley Lodge Park, Sturt Road, Frimley Green, Camberley, Surrey
            "100061558424",  # GU152EG -> GU152EF : 45 Upper Park Road, Camberley, Surrey
            "100061568651",  # GU248TA -> GU248TS : Fosters Farm, Woodcock Lane, Valley End, Chobham, Surrey
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "200001740856",  # GU166PY -> GU169NP : Holly Lodge Nursing Home, St Catherines Road, Frimley, Camberley, Surrey
            "200002884455",  # GU166PY -> GU169NP : Cedar Lodge Nursing Home, St Catherines Road, Frimley, Camberley, Surrey
            "100061556752",  # GU151AB -> GU151AE : Wits End, Springfield Road, Camberley, Surrey
            "10002677650",  # GU206PE -> GU206PF : Cricket Lodge,Woodcote House, Snows Ride, Windlesham, Surrey
            "200001921982",  # GU153HE -> GU153HB : 46 Academy Gate, 233 London Road, Camberley, Surrey
            "100061555263",  # GU167UJ -> GU168UG : ** Oak Hall, Portsmouth Road, Frimley, Camberley, Surrey
            "10002679513",  # GU153HQ -> GU153LT : 337A London Road, Camberley, Surrey
            "100061552219",  # GU153UG -> GU153TS : 69 London Road, Camberley, Surrey
        ]:
            rec["accept_suggestion"] = False

        return rec
