from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "E08000030"
    addresses_name = "local.2018-05-03/Version 2/polling_station_export-2018-03-12.csv"
    stations_name = "local.2018-05-03/Version 2/polling_station_export-2018-03-12.csv"
    elections = ["local.2018-05-03"]
    csv_encoding = "windows-1252"

    def get_station_hash(self, record):
        return "-".join([record.pollingstationnumber.strip()])

    def station_record_to_dict(self, record):

        # Changes requested by email
        if record.pollingstationnumber == "24":
            record = record._replace(pollingstationname="Community Room")
            record = record._replace(pollingstationaddress_1="Mattersley Court")
            record = record._replace(pollingstationaddress_2="Cresswell Crescent")
            record = record._replace(pollingstationaddress_3="Walsall")
            record = record._replace(pollingstationaddress_4="")
            record = record._replace(pollingstationaddress_5="")
            record = record._replace(pollingstationpostcode="WS3 2US")

        if record.pollingstationnumber == "70":
            record = record._replace(pollingstationpostcode="WS3 4JN")

        rec = super().station_record_to_dict(record)
        if rec["internal_council_id"] == "70":
            rec["location"] = Point(-1.971183, 52.625281, srid=4326)
        return rec

    def address_record_to_dict(self, record):
        if record.houseid in ["123217", "123218", "123219"]:
            rec = super().address_record_to_dict(record)
            rec["postcode"] = "WS9 0BA"
            return rec

        if record.houseid == "117495":
            rec = super().address_record_to_dict(record)
            rec["polling_station_id"] = ""
            return rec

        if record.housepostcode == "WS9 9DE":
            return None

        if record.housepostcode == "WS1 3DS":
            return None

        return super().address_record_to_dict(record)
