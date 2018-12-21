from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E06000016"
    addresses_name = "parl.2017-06-08/Version 1/Democracy_Club__08June2017.tsv"
    stations_name = "parl.2017-06-08/Version 1/Democracy_Club__08June2017.tsv"
    elections = ["parl.2017-06-08"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    station_postcode_field = "polling_place_address_2"
    station_address_fields = ["polling_place_name", "polling_place_address_1"]

    def address_record_to_dict(self, record):
        if len(record.addressline6) <= 6:
            return None
        return super().address_record_to_dict(record)
