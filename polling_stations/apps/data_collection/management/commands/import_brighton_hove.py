from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E06000043"
    addresses_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019BandH.tsv"
    stations_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019BandH.tsv"
    elections = ["europarl.2019-05-23"]
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
            "22253791",  # BN21TN -> BN14QE : Flat At, 16 Madeira Place, Brighton
            "22131280",  # BN31AE -> BN12PG : Lower Flat, 15 Western Road, Hove
        ]:
            rec["accept_suggestion"] = False

        return rec
