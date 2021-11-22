from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SHR"
    addresses_name = "2021-11-16T14:45:50.123476/Democracy_Club__16December2021.tsv"
    stations_name = "2021-11-16T14:45:50.123476/Democracy_Club__16December2021.tsv"
    elections = ["16-12-21"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Rhydycroesau Village Hall, Rhydycroesau, Oswestry
        if record.polling_place_id == "29344":
            record = record._replace(polling_place_easting=324197)
            record = record._replace(polling_place_northing=330779)

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "SY4 4EZ",
            "TF9 3HD",
            "TF9 3HE",
            "SY4 5JQ",
            "TF9 3RJ",
            "SY11 2LB",
            "SY11 3LP",
            "SY11 4PX",
        ]:
            return None

        return super().address_record_to_dict(record)
