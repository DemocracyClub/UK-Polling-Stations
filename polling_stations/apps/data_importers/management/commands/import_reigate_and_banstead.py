from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "REI"
    addresses_name = "2021-04-30T16:00:10.118165/Democracy_Club__06May2021.tsv"
    stations_name = "2021-04-30T16:00:10.118165/Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        if record.polling_place_id == "4151":
            record = record._replace(polling_place_postcode="")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):

        if record.addressline6 in [
            "RH1 1PH",
            "RH1 2JG",
            "RH2 9JB",
            "RH6 9BS",
            "RH6 8QG",
        ]:
            return None
        return super().address_record_to_dict(record)
