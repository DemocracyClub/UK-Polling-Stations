import re

from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RIB"
    addresses_name = "2024-07-04/2024-06-25T12:25:05.523108/RIB_combined.tsv"
    stations_name = "2024-07-04/2024-06-25T12:25:05.523108/RIB_combined.tsv"
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        simple_regex = r"^.*([A-Z]{2}[0-9]{1,2}\s*[0-9][A-Z]{2})$"

        rec = super().station_record_to_dict(record)
        last_line = rec["address"].split("\n")[-1]
        if m := re.match(simple_regex, last_line):
            rec["address"] = rec["address"].replace(m.group(1), "")
            rec["postcode"] = m.group(1)
        return rec

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10093891716",  # 44 HACKINGS CARAVAN PARK ELKER LANE, BILLINGTON
            "10093893136",  # BROCKTHRON LAITHE, WIGGLESWORTH ROAD, TOSSIDE, SKIPTON
        ]:
            return None
        if record.addressline6 in [
            # split
            "BB7 9GL",
        ]:
            return None

        return super().address_record_to_dict(record)
