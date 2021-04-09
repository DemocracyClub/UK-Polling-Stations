from django.contrib.gis.geos import Point
from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "POR"
    addresses_name = (
        "2021-03-24T11:20:37.542789/Portsmouth Democracy_Club__06May2021.tsv"
    )
    stations_name = (
        "2021-03-24T11:20:37.542789/Portsmouth Democracy_Club__06May2021.tsv"
    )
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in ["PO5 2BT", "PO4 0LF", "PO2 8LR"]:
            return None  # split
        rec = super().address_record_to_dict(record)
        return rec

    def station_record_to_dict(self, record):
        # Christ Church Church Hall
        if record.polling_place_id == "4918":
            record = record._replace(polling_place_uprn="1775049305")

        rec = super().station_record_to_dict(record)

        # St Margaret's Parish Centre
        if rec["internal_council_id"] == "4730":
            rec["location"] = Point(-1.067090, 50.786643, srid=4326)
        # Eastney Methodist Church
        if rec["internal_council_id"] == "4743":
            rec["location"] = Point(-1.059545, 50.7866578, srid=4326)

        return rec
