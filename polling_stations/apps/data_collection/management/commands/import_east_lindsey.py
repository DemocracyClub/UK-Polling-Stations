from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000137"
    addresses_name = "parl.2019-12-12/Version 3/Democracy_Club__12December2019V2.tsv"
    stations_name = "parl.2019-12-12/Version 3/Democracy_Club__12December2019V2.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)

        if record.addressline6 == "PE22 0TN":
            return None

        return rec
