from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000050"
    addresses_name = (
        "parl.2017-06-08/Version 3/NorthDorset-Democracy_Club__08June2017.tsv"
    )
    stations_name = (
        "parl.2017-06-08/Version 3/NorthDorset-Democracy_Club__08June2017.tsv"
    )
    elections = ["parl.2017-06-08"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def station_record_to_dict(self, record):

        """
        File supplied contained obviously inaccurate point
        remove it and fall back to geocoding
        """
        if record.polling_place_id == "5760":
            record = record._replace(polling_place_easting="0")
            record = record._replace(polling_place_northing="0")

        return super().station_record_to_dict(record)
