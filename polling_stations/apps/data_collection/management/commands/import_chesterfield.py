from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000034"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019Chester.tsv"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019Chester.tsv"
    elections = ["local.2019-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "74041261",  # S403BQ -> S402BQ : Stone Row, 11A Chatsworth Road, Brampton, Chesterfield
            "100030109655",  # S403LA -> S403LZ : 1 Faversham Court, 145 Somersall Lane, Chesterfield
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "74087237",  # S401GA -> S401DU : 1 Pottery Mews, Barker Lane, Brampton, Chesterfield
            "74087238",  # S401GA -> S401DU : 2 Pottery Mews, Barker Lane, Brampton, Chesterfield
            "74007391",  # S419RL -> S419QD : Dunston Cottage, Dunston Road, Dunston, Chesterfield
        ]:
            rec["accept_suggestion"] = False

        return rec
