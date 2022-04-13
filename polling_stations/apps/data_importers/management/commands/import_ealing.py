import re

from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "EAL"
    addresses_name = "2022-05-05/2022-04-13T16:32:47.995941/LB of Ealing Democracy_Club__05May2022.tsv"
    stations_name = "2022-05-05/2022-04-13T16:32:47.995941/LB of Ealing Democracy_Club__05May2022.tsv"
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in ["W4 5HL"]:
            return None  # split
        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Incomplete postcodes for temporary stations
        if re.match(r"^[A-Z]{1,2}[0-9]{1,2}$", record.polling_place_postcode):
            record = record._replace(polling_place_postcode="")

        return super().station_record_to_dict(record)
