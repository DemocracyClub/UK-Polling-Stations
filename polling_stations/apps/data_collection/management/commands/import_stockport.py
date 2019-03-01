from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E08000007"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019Stockport.tsv"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019Stockport.tsv"
    elections = ["local.2019-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        # Correction made because addresses are missing uprns in the csv.
        if record.addressline6 == "SK7 5AJ" and record.polling_place_id == "7908":
            rec["postcode"] = "SK8 6AJ"

        # matched to addressbase record by eye
        if uprn in [
            "10009672777",  # SK26NG -> SK26ND
            "10090543095",
            "10007621290",  # SK26QX -> SK26QZ
            "100011519677",  # SK26QX -> SK26QZ
            "100011486287",  # SK25PG -> SK14DG
            "100012478853",  # SK68DR -> SK68AA
            "100012480964",  # SK63DP -> SK63DR
            "100012478760",  # SK76AF -> SK76LU
            "100012478766",
            "10090546401",  # SK74AW -> SK74RF
            "100012481439",  # SK61NL -> SK61RJ
            "100012786198",  # SK65BB -> SK66AW
            "100012483235",  # SK65NY -> SK65DF
            "10000017775",  # SK67HB -> SK65HB
            "100011531719",  # SK45BS -> SK45BT
            "100011502100",  # SK11EW -> SK11ES
            "100011502101",
            "100012788925",  # SK83LA -> SK83LL
            "100012788926",
            "100012788927",
            "100012788928",
            "100012788929",
            "100012769647",  # SK12QE -> SK12JT
            "200000785972",  # SK64HT -> SK64DS
            "100012788954",  # SK83DQ -> SK83QA
            "100012786072",  # SK66LP -> SK65LP
            "10090543047",  # SK82NP -> SK82NZ
            "100011483808",  # SK65EL -> SK65EJ
            "10002096813",  # SK44NZ -> SK56AZ
            "100011523163",  # SK66AB -> SK66BD
            "100011523164",
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "10093012146",  # SK41NN -> SK14NN
            "10093012146",  # SK41NN -> SK14NN
        ]:
            rec["accept_suggestion"] = False

        return rec
