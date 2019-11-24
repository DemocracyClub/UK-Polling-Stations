from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000040"
    addresses_name = "parl.2019-12-12/Version 2/merged.CSV"
    stations_name = "parl.2019-12-12/Version 2/merged.CSV"
    elections = ["parl.2019-12-12"]
    csv_encoding = "Windows-1252"
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)

        if record.addressline6 == "EX1 3RR":
            return None

        return rec
