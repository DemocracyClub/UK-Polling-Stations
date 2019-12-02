from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "W06000005"
    addresses_name = "parl.2019-12-12/Version 2/Democracy_Club__12December2019flint.tsv"
    stations_name = "parl.2019-12-12/Version 2/Democracy_Club__12December2019flint.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):
        if record.polling_place_id == "5162":
            # Parish Hall/Neuadd Y Plwyf Halkyn/Helygain
            record = record._replace(polling_place_postcode="CH8 8BU")
        if record.polling_place_id == "5237":
            # Ysgol Y LLan, Whitfield
            record = record._replace(polling_place_uprn="10013703522")
        if record.polling_place_id == "5094":
            # War Memorial Institute, Rhydymwyn
            record = record._replace(polling_place_uprn="10090462071")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "CH4 9BS",
            "CH8 7AX",
            "CH6 5NF",
        ]:
            return None

        if record.addressline6 == "CH7 2QC":
            record = record._replace(addressline6="CH7 2QG")

        if record.addressline6 == "CH4 0TO":
            record = record._replace(addressline6="CH4 0TP")

        if record.addressline6 == "CH5 DR":
            record = record._replace(addressline6="CH5 4DR")

        if record.addressline6 == "CH5 2£J":
            record = record._replace(addressline6="CH5 2EJ")

        return super().address_record_to_dict(record)
