from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BPC"
    addresses_name = (
        "2024-05-02/2024-03-06T20:20:34.559585/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-06T20:20:34.559585/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Fix to match the coordinates of Station A
        # Station B - St. Andrew`s Parish Centre, 123 Shelbourne Road, Bournemouth BH8 8RD
        if record.polling_place_id == "16806":
            record = record._replace(
                polling_place_northing="92720",
            )

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # split
            "BH1 1NF",
            "BH14 0RD",
            "BH11 8BA",
            "BH23 3JJ",
            "BH1 3EB",
            "BH7 6LL",
            "BH6 3LF",
            "BH5 1DL",
            "BH10 5JF",
            "BH6 3NH",
        ]:
            return None
        return super().address_record_to_dict(record)
