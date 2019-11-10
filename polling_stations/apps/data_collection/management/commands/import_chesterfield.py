from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000034"
    addresses_name = (
        "parl.2019-12-12/Version 1/Democracy_Club__12December2019chesterf.tsv"
    )
    stations_name = (
        "parl.2019-12-12/Version 1/Democracy_Club__12December2019chesterf.tsv"
    )
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100030109655",  # S403LA -> S403LZ : 1 Faversham Court, 145 Somersall Lane, Chesterfield
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "74087237",  # S401GA -> S401DU : 1 Pottery Mews, Barker Lane, Brampton, Chesterfield
            "74087238",  # S401GA -> S401DU : 2 Pottery Mews, Barker Lane, Brampton, Chesterfield
            "74007391",  # S419RL -> S419QD : Dunston Cottage, Dunston Road, Dunston, Chesterfield
        ]:
            rec["accept_suggestion"] = False

        if uprn == "74085483":
            rec["postcode"] = "S40 2NE"
            rec["accept_suggestion"] = False

        return rec
