from django.contrib.gis.geos import Point

from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WBK"
    addresses_name = (
        "2023-05-04/2023-03-10T17:54:14.260272/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-10T17:54:14.260272/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Peasemore Village Hall Peasemore RG20 7JE
        if record.polling_place_id == "7579":
            record = record._replace(
                polling_place_postcode="RG20 7JE ", polling_place_address_2=""
            )

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # split
            "RG14 1EP",
        ]:
            return None

        return super().address_record_to_dict(record)
