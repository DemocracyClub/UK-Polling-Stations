from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "ASH"
    addresses_name = "2021-03-29T10:18:22.398168/Ashfield Democracy_Club__06May2021.CSV"
    stations_name = "2021-03-29T10:18:22.398168/Ashfield Democracy_Club__06May2021.CSV"
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def station_record_to_dict(self, record):
        # The Summit Centre Room 2 Pavilion Road Kirkby in Ashfield Nottingham NG17 7LL
        # changing to the same as The Summit Centre Room 1 Pavilion Road Kirkby In Ashfield Nottingham NG17 7LL
        if record.polling_place_id == "3638":
            record = record._replace(polling_place_easting="450822")
            record = record._replace(polling_place_northing="356660")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100031248754",  # 31 COXMOOR ROAD, SUTTON-IN-ASHFIELD
        ]:
            return None

        if record.addressline6 in ["NG17 8BE", "NG17 8JR", "NG17 5HS"]:
            return None

        return super().address_record_to_dict(record)
