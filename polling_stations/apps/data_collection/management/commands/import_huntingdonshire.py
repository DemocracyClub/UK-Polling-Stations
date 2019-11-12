from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000011"
    addresses_name = (
        "parl.2019-12-12/Version 1/Democracy_Club__12December2019hunting.tsv"
    )
    stations_name = (
        "parl.2019-12-12/Version 1/Democracy_Club__12December2019hunting.tsv"
    )
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):

        if record.polling_place_id == "6703":  # Berkley Street Methodist Church
            record = record._replace(polling_place_postcode="PE19 2NB")

        return super().station_record_to_dict(record)
