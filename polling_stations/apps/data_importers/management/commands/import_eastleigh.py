from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "EAT"
    addresses_name = "2021-03-03T12:56:56.264077/Eastleigh Borough Council Democracy_Club__06May2021 (1).tsv"
    stations_name = "2021-03-03T12:56:56.264077/Eastleigh Borough Council Democracy_Club__06May2021 (1).tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100060322293",  # 18 LEWRY CLOSE, HEDGE END, SOUTHAMPTON
            "10094385410",  # 44A KELBURN CLOSE, CHANDLER'S FORD
            "10012197923",  # 300 CHESTNUT AVENUE, CHANDLER'S FORD, EASTLEIGH
            "10009593531",  # FLAT 1 85 TWYFORD ROAD, EASTLEIGH
            "10094385283",  # 12 JACOBS CLOSE, BURSLEDON
        ]:
            return None

        if record.addressline6 in ["SO31 5FH", "SO30 3FA", "SO53 2FG"]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        if (
            record.polling_place_id == "5150"
        ):  # Abbey Hall Victoria Road Netley Abbey Southampton SO31 5FA
            record = record._replace(polling_place_easting="445235")
            record = record._replace(polling_place_northing="108734")

        if (
            record.polling_place_id == "5105"
        ):  # Chandler's Ford Community Centre, Hursley Road, Chandler's Ford, Eastleigh, SO53 2FS
            record = record._replace(polling_place_postcode="SO53 2FT")

        return super().station_record_to_dict(record)
