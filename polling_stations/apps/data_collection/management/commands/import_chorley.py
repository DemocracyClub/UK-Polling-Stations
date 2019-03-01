from data_collection.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "E07000118"
    addresses_name = (
        "local.2019-05-02/Version 1/polling_station_export-2019-02-11 Chorley.csv"
    )
    stations_name = (
        "local.2019-05-02/Version 1/polling_station_export-2019-02-11 Chorley.csv"
    )
    elections = ["local.2019-05-02"]

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.uprn.strip().lstrip("0")

        if record.housepostcode == "PR6 7ED":
            return None

        if uprn in [
            "200004070947",  # PR72QL -> PR73QL : 2 BIRKACRE ROAD, CHORLEY
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
