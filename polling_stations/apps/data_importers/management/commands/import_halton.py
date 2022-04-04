from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HAL"
    addresses_name = (
        "2022-05-05/2022-03-21T14:24:18.499238/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-21T14:24:18.499238/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Holy Trinity Church Trinity Street Runcorn WA7 1BJ
        if record.polling_place_id == "2817":
            record = record._replace(polling_place_easting="351595")
            record = record._replace(polling_place_northing="383048")

        # Mobile Polling Station Galway Ave. Widnes
        if record.polling_place_id == "2809":
            record = record._replace(polling_place_easting="350205")
            record = record._replace(polling_place_northing="387147")
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10090873639",  # THE BLACKSMITHS, NORTON LANE, NORTON, RUNCORN
        ]:
            return None

        if record.addressline6 in [
            "WA8 7TF",
            "WA8 7TB",
            "WA8 8PZ",
            "WA7 1BH",
            "WA7 2QA",
            "WA4 4BL",
        ]:
            return None

        return super().address_record_to_dict(record)
