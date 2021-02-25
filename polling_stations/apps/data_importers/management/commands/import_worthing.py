from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WOT"
    addresses_name = "2021-02-15T11:21:49.443491/WBCDemocracy_Club__06May2021.tsv"
    stations_name = "2021-02-15T11:21:49.443491/WBCDemocracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):

        # Moved to correct address => Richmond Room (adj. to Assembly Hall), Stoke Abbott Road, Worthing
        if record.polling_place_id == "2171":
            record = record._replace(polling_place_easting="514729")
            record = record._replace(polling_place_northing="102975")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.addressline6 == "BN11 3FP":
            return None
        return super().address_record_to_dict(record)
