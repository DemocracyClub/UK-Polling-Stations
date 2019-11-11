from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "W06000021"
    addresses_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019mon.tsv"
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019mon.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        if record.addressline1 == "Bryn Cwrt":
            rec["postcode"] = "NP44 2DB"
            rec["uprn"] = "10033347654"

        return rec
