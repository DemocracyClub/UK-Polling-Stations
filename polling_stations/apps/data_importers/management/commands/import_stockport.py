from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SKP"
    addresses_name = (
        "2023-05-04/2023-03-16T11:22:27.978693/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-16T11:22:27.978693/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10096031489",  # 13 MOORE ROAD, HEALD GREEN, CHEADLE
            "10094501452",  # 35A GREAVE, ROMILEY, STOCKPORT
        ]:
            return None

        if record.addressline6 in [
            # split
            "SK8 4BU",
            "SK6 6LP",
            "SK4 5BS",
            "SK7 4NX",
            "SK7 2AA",
            "SK7 3DQ",
            "SK6 2BD",
            "SK7 5BD",
            "SK5 7BJ",
            "SK3 9HB",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Kingsway School (Lower) Broadway Campus High Grove Road Cheadle SK8 1NP
        if record.polling_place_id == "12173":
            record = record._replace(polling_place_easting="")
            record = record._replace(polling_place_northing="")

        return super().station_record_to_dict(record)
