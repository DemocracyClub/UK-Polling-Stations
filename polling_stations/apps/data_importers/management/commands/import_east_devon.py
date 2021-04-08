from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "EDE"
    addresses_name = "2021-04-07T16:28:34.172331/2 Democracy_Club__06May2021.tsv"
    stations_name = "2021-04-07T16:28:34.172331/2 Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10093128988",  # CARAVAN 2 GREENDALE LANE, CLYST ST MARY
            "10094722867",  # MOLLYS COTTAGE SNODWELL FARM POST LANE, COTLEIGH
            "10093125768",  # THE COACH HOUSE CHATTAN COURT WOODBURY LANE, AXMINSTER
        ]:
            return None

        if record.post_code in ["EX24 6JY", "EX8 4FA", "EX8 2FQ"]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Seaton Marshlands Centre Harbour Road Seaton EX12 2LT.
        if record.polling_place_id == "13893":
            record = record._replace(
                polling_place_postcode=record.polling_place_address_3.strip(".")
            )
            record = record._replace(polling_place_address_3="")

        return super().station_record_to_dict(record)
