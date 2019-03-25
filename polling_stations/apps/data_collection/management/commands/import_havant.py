from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000090"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019Havant.tsv"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019Havant.tsv"
    elections = ["local.2019-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn == "100060444834":
            rec["postcode"] = "PO11 0LJ"
            rec["accept_suggestion"] = False

        if uprn in [
            "100062455644",  # PO88BB -> PO78NU : Plough & Barleycorn, Tempest Avenue, Cowplain, Waterlooville, Hampshire
            "10013680951",  # PO107NH -> PO107DN : 1E St James Road, Emsworth, Hampshire
            "10013675502",  # PO89UB -> PO89GX : 7A The Kestrels, 76 Eagle Avenue, Waterlooville, Hampshire
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "100060458913"  # PO75AA -> PO75JU : 108 London Road, Widley, Waterlooville, Hampshire
        ]:
            rec["accept_suggestion"] = False

        return rec
