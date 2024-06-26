from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WOT"
    addresses_name = "2024-07-04/2024-06-07T16:41:56.977816/WOT_combined.tsv"
    stations_name = "2024-07-04/2024-06-07T16:41:56.977816/WOT_combined.tsv"
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # WDIV bugfix 666: removes map pending council response for:
        # Richmond Room (adj. to Assembly Hall), Stoke Abbott Road, Worthing, BN11 1HQ
        # suggested coords (x,y): 514733.31, 102962.60
        if record.polling_place_id == "3160":
            record = record._replace(
                polling_place_easting="",
                polling_place_northing="",
                polling_place_uprn="",
            )
        return super().station_record_to_dict(record)
