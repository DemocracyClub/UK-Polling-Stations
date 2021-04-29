from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "KIN"
    addresses_name = "2021-04-29T10:57:28.594826/Democracy-Club-Data-West-Norfolk.csv"
    stations_name = "2021-04-29T10:57:28.594826/Democracy-Club-Data-West-Norfolk.csv"
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def station_record_to_dict(self, record):

        # Lakes End Village Hall Main Road Lakes End WISBECH PE14 9QL
        if record.polling_place_id == "20394":
            record = record._replace(polling_place_postcode="PE14 9QH")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):

        if record.addressline6 in [
            "PE30 4XW",
            "PE30 4XW",
            "PE31 6HJ",
            "PE38 9QZ",
            "PE14 7QT",
            "PE14 8JN",
            "PE34 4RD",
            "PE34 3BJ",
            "PE34 4EX",
            "PE30 3LE",
            "PE33 9PN",
            "PE30 3BG",
            "PE14 7LB",
            "PE14 7EU",
        ]:
            return None

        return super().address_record_to_dict(record)
