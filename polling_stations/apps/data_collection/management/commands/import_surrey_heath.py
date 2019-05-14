from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000214"
    addresses_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019SH.tsv"
    stations_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019SH.tsv"
    elections = ["europarl.2019-05-23"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)

        # From: 972106:polling_stations/apps/data_collection/management/commands/misc_fixes.py-245-
        if rec["internal_council_id"] == "2422":  # Heatherside Community Centre
            rec["location"] = Point(-0.702364, 51.329003, srid=4326)

        return rec

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if "Lucas Drive" in record.addressline1:
            rec["postcode"] = "GU249JQ"

        if uprn == "200000199948":  # Medcote Cottage, Water Lane
            return None

        if uprn in [
            "100061567393",  # GU195ES -> GU249PJ : 37 Oakridge, West End, Woking, Surrey
            "100062330131",  # GU166NS -> GU166HY : The Bungalow, Frimley Lodge Park, Sturt Road, Frimley Green, Camberley, Surrey
            "100061558424",  # GU152EG -> GU152EF : 45 Upper Park Road, Camberley, Surrey
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "200001740856",  # GU166PY -> GU169NP : Holly Lodge Nursing Home, St Catherines Road, Frimley, Camberley, Surrey
            "200002884455",  # GU166PY -> GU169NP : Cedar Lodge Nursing Home, St Catherines Road, Frimley, Camberley, Surrey
            "100061556752",  # GU151AB -> GU151AE : Wits End, Springfield Road, Camberley, Surrey
            "10002677650",  # GU206PE -> GU206PF : Cricket Lodge,Woodcote House, Snows Ride, Windlesham, Surrey
            "200001921982",  # GU153HE -> GU153HB : 46 Academy Gate, 233 London Road, Camberley, Surrey
            "100061555236",  # GU167UJ -> GU151JN : 11 Oak Hall, Portsmouth Road, Frimley, Camberley, Surrey
            "10002679513",  # GU153HQ -> GU153LT : 337A London Road, Camberley, Surrey
            "100062328067",  # GU152AN -> GU152JL : Flat 7 Crawley Lodge, Crawley Ridge, Camberley, Surrey
        ]:
            rec["accept_suggestion"] = False

        return rec
