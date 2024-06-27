from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WOT"
    addresses_name = "2024-07-04/2024-06-07T16:41:56.977816/WOT_combined.tsv"
    stations_name = "2024-07-04/2024-06-07T16:41:56.977816/WOT_combined.tsv"
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # WDIV bugfix 666: council agree to coord fix for:
        # Richmond Room (adj. to Assembly Hall), Stoke Abbott Road, Worthing, BN11 1HQ
        if record.polling_place_id == "3160":
            record = record._replace(
                polling_place_easting="514733",
                polling_place_northing="102963",
            )
        return super().station_record_to_dict(record)
