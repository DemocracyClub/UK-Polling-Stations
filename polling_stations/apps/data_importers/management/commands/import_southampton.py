from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "STH"
    addresses_name = (
        "2022-05-05/2022-04-12T12:29:28.468901/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-04-12T12:29:28.468901/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # The Royal British Legion Club (Function Room), Windover Close, Southampton
        if record.polling_place_id == "13603":
            record = record._replace(polling_place_postcode="SO19 5JS")  # was S019 5JS

        # Highfield Church Centre (Lounge), Highfield Lane, Southampton
        if record.polling_place_id == "13739":
            record = record._replace(polling_place_postcode="SO17 1RL")  # was SO17 7RL

        # Testlands Hub (Spin/Conference Room), (Formerly Millbrook Secondary School), Green Lane
        if record.polling_place_id == "13764":
            record = record._replace(polling_place_postcode="SO16 9FQ")  # was SO16 9RG

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.addressline6 in ["SO15 2NS", "SO16 7AS", "SO16 7GQ"]:
            return None  # split

        return super().address_record_to_dict(record)
