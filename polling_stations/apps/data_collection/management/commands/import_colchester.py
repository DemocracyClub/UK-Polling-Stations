from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000071"
    addresses_name = (
        "local.2018-05-03/Version 1/Democracy_Club__03May2018 Colchester.csv"
    )
    stations_name = (
        "local.2018-05-03/Version 1/Democracy_Club__03May2018 Colchester.csv"
    )
    elections = ["local.2018-05-03"]
    csv_delimiter = ","

    def station_record_to_dict(self, record):
        if record.polling_place_id == "8431":
            record = record._replace(polling_place_postcode="CO2 0EH")
        return super().station_record_to_dict(record)
