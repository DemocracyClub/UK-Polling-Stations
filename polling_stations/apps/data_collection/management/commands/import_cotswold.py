from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000079"
    addresses_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019cots.tsv"
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019cots.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)

        if record.addressline1 == "Flat Above Garage, Treetops":
            rec["postcode"] = "GL560HE"

        return rec

    def station_record_to_dict(self, record):

        # source: https://britishlistedbuildings.co.uk/101340859-village-hall-icomb
        # Icomb Village Hall
        if record.polling_place_id == "16018":
            record = record._replace(polling_place_northing="222640")

        return super().station_record_to_dict(record)
