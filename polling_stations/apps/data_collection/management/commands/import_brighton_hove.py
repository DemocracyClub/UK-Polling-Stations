from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E06000043"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019BH.tsv"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019BH.tsv"
    elections = ["local.2019-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "22249017",  # BN13RH -> BN13PJ : Flat 1, 22 Buckingham Road, Brighton
            "22200182",  # BN33PY -> BN33JN : Maisonette (1ST/2ND/F), 64 Wilbury Road, Hove
            "22132382",  # BN34HB -> BN34HA : Ground Floor, 26 Braemore Road, Hove
            "22125165",  # BN15DQ -> BN37BE : First Floor, 37 Old Shoreham Road, Brighton
            "22258781",  # BN20AL -> BN20AJ : Deputy House Mistress Flat New House, Brighton College, Eastern Road, Brighton
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "22259748",  # BN21AU -> BN21PD : Flat 2 (First Rear), 21 Burlington Street, Brighton
            "22258121",  # BN31AE -> BN11HH : Flat 6, 3-4 Western Road, Hove
            "22262337",  # BN12AU -> BN11HJ : Flat 53 Russell House, Russell Mews, Brighton
            "22258120",  # BN31AE -> BN11HH : Flat 5, 3-4 Western Road, Hove
            "22253791",  # BN21TN -> BN14QE : Flat At, 16 Madeira Place, Brighton
        ]:
            rec["accept_suggestion"] = False

        return rec
