from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CRW"
    addresses_name = (
        "2022-05-05/2022-03-23T15:28:26.755741/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-23T15:28:26.755741/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Furnace Green Community Centre
        if record.polling_place_id == "1056":
            record = record._replace(polling_place_easting="528414")
            record = record._replace(polling_place_northing="135782")

        # Wakehams Green Community Centre
        if record.polling_place_id == "1103":
            record = record._replace(polling_place_easting="529968")
            record = record._replace(polling_place_northing="138172")

        # Southgate West Community Centre
        if record.polling_place_id == "1073":
            record = record._replace(polling_place_easting="526307")
            record = record._replace(polling_place_northing="135610")

        return super().station_record_to_dict(record)
