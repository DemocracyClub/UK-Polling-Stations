from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000099"
    addresses_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019Nherts.tsv"
    stations_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019Nherts.tsv"
    elections = ["europarl.2019-05-23"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):

        if record.polling_place_id == "6876":  # Studlands Rise First School
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-0.013935, 52.045835, srid=4326)
            return rec

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10013379572",  # SG85AB -> SG85AN : 28A Stamford Yard, Kneesworth Street, Royston, Herts
            "100081260214",  # SG89JU -> SG89JS : 25 Market Hill, Royston, Herts
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "100081125858",  # SG75HY -> SG75HU : The Cuckoo Poultry Farm, Hinxworth Road, Ashwell, Baldock, Herts.
            "10070035918",  # SG62AA -> SG62AL : Keeper`s Cottage, Willian Road, Letchworth, Herts
            "10023322772",  # SG62AA -> SG62AL : Annexe, Keeper`s Cottage, Willian Road, Letchworth, Herts
            "10070043607",  # SG85AA -> SG85AQ : 7 Kneesworth Street, Royston, Herts
        ]:
            rec["accept_suggestion"] = False

        return rec
