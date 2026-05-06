from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WOT"
    addresses_name = (
        "2026-05-07/2026-03-17T12:17:24.284853/Democracy_Club__07May2026WBC.tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-17T12:17:24.284853/Democracy_Club__07May2026WBC.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # fix bad point for Richmond Room:
        # https://app.asana.com/1/1204880536137786/project/1207538772343223/task/1214570745863239?focus=true
        if record.polling_place_id == "3617":
            record = record._replace(
                polling_place_easting="514751",
                polling_place_northing="102980",
            )
        return super().station_record_to_dict(record)
