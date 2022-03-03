from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "EAT"
    addresses_name = (
        "2022-05-05/2022-02-22T09:04:34.675651/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-02-22T09:04:34.675651/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        if (
            record.polling_place_id == "5363"
        ):  # Abbey Hall Victoria Road Netley Abbey Southampton SO31 5FA
            record = record._replace(polling_place_easting="445235")
            record = record._replace(polling_place_northing="108734")

        if (
            record.polling_place_id == "5351"
        ):  # Chandler's Ford Community Centre, Hursley Road, Chandler's Ford, Eastleigh, SO53 2FS
            record = record._replace(polling_place_postcode="SO53 2FT")

        return super().station_record_to_dict(record)
