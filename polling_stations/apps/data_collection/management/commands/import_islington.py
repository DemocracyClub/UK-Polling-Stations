from django.contrib.gis.geos import Point
from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E09000019"
    addresses_name = "europarl.2019-05-23/Version 1/islington.gov.uk-1557480923000-.TSV"
    stations_name = "europarl.2019-05-23/Version 1/islington.gov.uk-1557480923000-.TSV"
    elections = ["europarl.2019-05-23"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        # postcode corrections
        if uprn in ["10093623311", "10093623312", "10093623313"]:
            rec["postcode"] = "EC1M 5UD"
        if uprn == "10012788158":
            rec["postcode"] = "EC1V 0ET"

        return rec

    def station_record_to_dict(self, record):
        rec = super().station_record_to_dict(record)

        # Location corrections carried forward
        if rec["internal_council_id"] == "1531":  #    St. Thomas` Church Hall
            rec["location"] = Point(-0.104049, 51.560139, srid=4326)
        if rec["internal_council_id"] == "1519":  # St Joan of Arc Community Centre
            rec["location"] = Point(-0.0966823, 51.5559102, srid=4326)

        return rec
