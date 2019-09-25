from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "E07000118"
    addresses_name = (
        "parl.maybe/Version 1/chorley-polling_station_export-2019-09-16.csv"
    )
    stations_name = "parl.maybe/Version 1/chorley-polling_station_export-2019-09-16.csv"
    elections = ["parl.maybe"]

    def get_station_point(self, record):
        return None

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.uprn.strip().lstrip("0")

        if record.housepostcode == "PR6 7ED":
            return None

        if uprn in [
            "200004070947",  # PR72QL -> PR73QL : 2 PLYMOUTH COTTAGES, BIRKACRE ROAD
            "10002076206",  # PR67LB -> PR67LS : HILLSIDE COTTAGE, 1 NAYLORS FOLD HILL TOP LANE
            "100010385659",  # PR75DB -> PR75DE : THE BUNGALOW SPENDMORE LANE, COPPULL
            "10070372269",  # PR69AT -> PR269AT : SNOWDROP COTTAGE BANK HALL DRIVE, BRETHERTON
        ]:
            rec["accept_suggestion"] = True

        # just bin the UPRNs on these ones
        if uprn in [
            "100010391254",  # PR75TW -> L402QN : 41 NEW STREET, ECCLESTON
            "100010391256",  # PR75TW -> L402QN : 43 NEW STREET, ECCLESTON
            "10070371313",  # L402QN -> PR75TW : 41 NEW STREET, MAWDESLEY, ORMSKIRK
            "10070371314",  # L402QN -> PR75TW : 43 NEW STREET, MAWDESLEY, ORMSKIRK
        ]:
            rec["accept_suggestion"] = False

        return rec
