from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E09000020"
    addresses_name = "europarl.2019-05-23/Version 1/rbkc.gov.uk-1556546288000-.tsv"
    stations_name = "europarl.2019-05-23/Version 1/rbkc.gov.uk-1556546288000-.tsv"
    elections = ["europarl.2019-05-23"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):

        # St Columba's Church
        if record.polling_place_id == "747":
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-0.163128, 51.496844, srid=4326)
            return rec

        # St Cuthbert`s Centre
        if record.polling_place_id == "776":
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-0.200082, 51.491363, srid=4326)
            return rec

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "217126141":
            rec["postcode"] = "SW5 9EZ"
        if uprn == "217108045":
            rec["postcode"] = "W8 5DH"

        if record.addressline6.strip() == "SW1X 8HN":
            rec["postcode"] = "SW1X 8HJ"

        if (
            record.addressline6 == "W11 4LY"
            and record.addressline1 == "2B Drayson Mews"
        ):
            rec["postcode"] = "W8 4LY"

        return rec
