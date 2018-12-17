from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E08000003"
    addresses_name = "local.2018-05-03/Version 1/Democracy_Club__03May2018 - MCC.TSV"
    stations_name = "local.2018-05-03/Version 1/Democracy_Club__03May2018 - MCC.TSV"
    elections = ["local.2018-05-03"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):

        """
        File supplied contained obviously inaccurate point
        remove it and fall back to geocoding
        """
        if record.polling_place_id == "4943":
            record = record._replace(polling_place_easting="0")
            record = record._replace(polling_place_northing="0")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):

        if record.addressline6.strip() == "WA15 8XL":
            return None

        if record.addressline6.strip() == "M15 4PF":
            return None

        if record.addressline6.strip() == "M40 8AZ":
            return None

        return super().address_record_to_dict(record)
