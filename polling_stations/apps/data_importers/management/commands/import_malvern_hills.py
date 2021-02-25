from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MAV"
    addresses_name = "2021-02-11T16:36:52.078441/a.tsv"
    stations_name = "2021-02-11T16:36:52.078441/a.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        if record.polling_place_id == "11488":
            record = record._replace(polling_place_easting="379264")
            record = record._replace(polling_place_northing="246303")

        rec = super().station_record_to_dict(record)

        return rec

    def address_record_to_dict(self, record):

        if record.addressline6 in [
            "WR5 3PA",
            "WR6 6YY",
            "WR15 8JF",
            "WR15 8DP",
            "WR2 6RB",
            "WR14 4JY",
        ]:
            return None
        rec = super().address_record_to_dict(record)

        return rec
