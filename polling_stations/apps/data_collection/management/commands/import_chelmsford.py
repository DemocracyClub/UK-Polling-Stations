from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000070"
    addresses_name = (
        "parl.2017-06-08/Version 1/Chelmsford Democracy_Club__08June2017.tsv"
    )
    stations_name = (
        "parl.2017-06-08/Version 1/Chelmsford Democracy_Club__08June2017.tsv"
    )
    elections = ["parl.2017-06-08"]
    csv_delimiter = "\t"
    csv_encoding = "latin-1"

    def station_record_to_dict(self, record):

        if record.polling_place_id == "7695":
            record = record._replace(polling_place_postcode="CM1 1FG")

        return super().station_record_to_dict(record)
