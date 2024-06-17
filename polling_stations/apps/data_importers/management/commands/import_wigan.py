from data_importers.management.commands import BaseXpressWebLookupCsvImporter


class Command(BaseXpressWebLookupCsvImporter):
    council_id = "WGN"
    addresses_name = "2024-07-04/2024-06-22T08:32:01.577572/wigan-cleaned.csv"
    stations_name = "2024-07-04/2024-06-22T08:32:01.577572/wigan-cleaned.csv"
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "200002861926",  # THE COTTAGE, SANDY LANE, HINDLEY, WIGAN
            "100012500668",  # DODHURST BROW FARM, SANDY LANE, HINDLEY, WIGAN
            "100011823007",  # 165 WIGAN ROAD, ASHTON-IN-MAKERFIELD, WIGAN
            "10095424360",  # 109 ANCHOR FIELD, LEIGH
            "10095424324",  # 73 ANCHOR FIELD, LEIGH
            "10095424371",  # 120 ANCHOR FIELD, LEIGH
        ]:
            return None

        if record.postcode in [
            # splits
            "WN7 4TF",
            "WN7 1QA",
            "WN7 2LS",
            # suspect
            "WN7 4GL",
            "WN7 4GQ",
        ]:
            return None

        return super().address_record_to_dict(record)
