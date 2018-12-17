from data_collection.management.commands import (
    BaseXpressDCCsvInconsistentPostcodesImporter,
)


class Command(BaseXpressDCCsvInconsistentPostcodesImporter):
    council_id = "E09000008"
    addresses_name = (
        "local.2018-05-03/Version 1/Democracy_Club__03May2018 Croydon (2).tsv"
    )
    stations_name = (
        "local.2018-05-03/Version 1/Democracy_Club__03May2018 Croydon (2).tsv"
    )
    elections = ["local.2018-05-03"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):

        """
        File supplied contained obviously inaccurate point
        remove it and fall back to geocoding
        """
        if record.polling_place_id == "9300":
            record = record._replace(polling_place_easting="0")
            record = record._replace(polling_place_northing="0")

        if record.polling_place_id == "9308":
            record = record._replace(polling_place_postcode="CR0 9DZ")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):

        # All of the UPRN data from Croydon is a bit dubious.
        # For safety I'm just going to ignore them all
        record = record._replace(property_urn="")

        bad_postcodes = [
            "CR0 7JP",
            "CR7 7JP",
            "SE25 4QF",
            "SE25 5QF",
            "CR0 5AG",
            "CR0 5AQ",
        ]

        if record.addressline6.strip() in bad_postcodes:
            return None

        return super().address_record_to_dict(record)
