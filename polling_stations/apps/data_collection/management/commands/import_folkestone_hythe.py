from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000112"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019folkstone.tsv"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019folkstone.tsv"
    elections = ["local.2019-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "50104978",  # TN299AU -> TN299UA : Headmasters House, Rhee Wall, Brenzett, Romney Marsh, Kent
            "50042070",  # CT202NQ -> CT202QN : Flat D, 104 Cheriton Road, Folkestone, Kent
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "50124993",  # CT195UW -> CT202PX : 1 Melanie Close, Folkestone, Kent
            "50124434",  # CT188LW -> CT188EW : Annexe Holly Lodge, Reece Lane, Acrise, Folkestone, Kent
        ]:
            rec["accept_suggestion"] = False

        return rec
