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

        if record.polling_place_id in [
            "2809",  # Mobile Polling Station Galway Ave. Widnes
            "2817",  # Holy Trinity Church Trinity Street Runcorn WA7 1BJ
        ]:
            record = record._replace(polling_place_easting="")
            record = record._replace(polling_place_northing="")

        if record.polling_place_id in [
            "2561",  # Prescot Road Changing Rooms Hough Green Road Widnes WA8 7PD
        ]:
            record = record._replace(polling_place_postcode="")

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
