from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SFT"
    addresses_name = "2021-04-14T17:32:40.128471/Sefton.tsv"
    stations_name = "2021-04-14T17:32:40.128471/Sefton.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "41063021",  # 8 MOOR LANE, THORNTON, LIVERPOOL
            "41215760",  # 471A LORD STREET, SOUTHPORT
        ]:
            return None

        if record.addressline6 in [
            "L23 7TX",
            "L20 6AQ",
            "L30 7PD",
            "L20 6EA",
            "L9 5AD",
            "L31 2JE",
            "L31 2JF",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):

        # Bootle Main Library 220 Stanley Road Bootle L20 3GN
        if record.polling_place_id == "7799":
            record = record._replace(polling_place_postcode="")

        # Ford Lane Community Centre Ford Lane Litherland Liverpool L21 7LX
        if record.polling_place_id == "7737":
            record = record._replace(polling_place_postcode="")

        return super().station_record_to_dict(record)
