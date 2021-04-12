from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HAL"
    addresses_name = "2021-03-25T09:19:48.436436/Halton Democracy_Club__06May2021.tsv"
    stations_name = "2021-03-25T09:19:48.436436/Halton Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Scout Hut, Hall Avenue, Widnes
        if record.polling_place_id == "2404":
            record = record._replace(polling_place_postcode="WA8 4PU")

        if record.polling_place_id in [
            "2437",  # Mobile Polling Station Galway Ave. Widnes
            "2444",  # Holy Trinity Church Trinity Street Runcorn WA7 1BJ
            "2422",  # Church of Jesus Christ of Latter Day Saints Clifton Road Runcorn WA7 4TE
            "2429",  # Beechwood Community Centre Beechwood Avenue Runcorn WA7 3HB
        ]:
            record = record._replace(polling_place_easting="")
            record = record._replace(polling_place_northing="")

        if record.polling_place_id in [
            "2561",  # Prescot Road Changing Rooms Hough Green Road Widnes WA8 7PD
            "2429",  # Beechwood Community Centre Beechwood Avenue Runcorn WA7 3HB
        ]:
            record = record._replace(polling_place_postcode="")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10090873639",  # THE BLACKSMITHS, NORTON LANE, NORTON, RUNCORN
            "10093155713",  # HORSESHOE BARN, VILLAGE FARM, CHESTER ROAD, DARESBURY, WARRINGTON
            "10093156249",  # 141 CORONERS LANE, WIDNES
            "10093157269",  # 36 MILTON ROAD, WIDNES
            "10090873401",  # 137A WILMERE LANE, WIDNES
            "100012379277",  # EIGHT TOWERS, WEATES CLOSE, WIDNES
            "10093157290",  # CONNORS COTTAGE 162A HOUGH GREEN ROAD, WIDNES
            "10093155808",  # 39 HALTON BROW, HALTON, RUNCORN
        ]:
            return None

        if record.addressline6 in [
            "WA8 5AZ",
            "WA8 7TF",
            "WA8 7TB",
            "WA8 8SZ",
            "WA8 8SF",
            "WA8 8PZ",
            "WA7 1BH",
            "WA7 4SX",
            "WA7 2QA",
            "WA4 4BL",
            "WA7 4UA",
        ]:
            return None

        return super().address_record_to_dict(record)
