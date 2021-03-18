from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "STY"
    addresses_name = "2021-03-17T14:46:18.378677/Democracy_Club__06May2021.tsv"
    stations_name = "2021-03-17T14:46:18.378677/Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):

        # Removing undesired text
        if "NEW STATION" in record.polling_place_address_1:
            record = record._replace(polling_place_address_1="")
        if "NEW STATION" in record.polling_place_address_2:
            record = record._replace(polling_place_address_2="")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.addressline6 in ["NE31 2XF", "NE34 8AE"]:
            return None

        return super().address_record_to_dict(record)
