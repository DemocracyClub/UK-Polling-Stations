from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HAL"
    addresses_name = (
        "2023-05-04/2023-03-14T10:55:51.877415/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-14T10:55:51.877415/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        name = record.polling_place_name.replace("`", "'")
        record = record._replace(polling_place_name=name)
        # Holy Trinity Church Trinity Street Runcorn WA7 1BJ
        if record.polling_place_id == "3405":
            record = record._replace(polling_place_easting="351595")
            record = record._replace(polling_place_northing="383048")

        # Mobile Polling Station Galway Ave. Widnes
        if record.polling_place_id == "3396":
            record = record._replace(polling_place_easting="")
            record = record._replace(polling_place_northing="")

        # User issue #572
        # St Michael`s Catholic Church, St Michael`s Road, Widnes
        if record.polling_place_id == "3444":
            record = record._replace(polling_place_easting="")
            record = record._replace(polling_place_northing="")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # split
            "WA8 7TB",
            "WA7 1BH",
            "WA7 2QA",
            "WA8 8PZ",
            "WA8 8HZ",
            "WA4 4BL",
            "WA8 7TF",
            "WA7 4SX",
        ]:
            return None

        return super().address_record_to_dict(record)
