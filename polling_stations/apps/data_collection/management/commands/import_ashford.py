from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000105"
    addresses_name = "local.2019-05-02/Version 2/Democracy_Club__02May2019Ashford.tsv"
    stations_name = "local.2019-05-02/Version 2/Democracy_Club__02May2019Ashford.tsv"
    elections = ["local.2019-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10012843238",  # TN257AS -> TN257AR : Fairfield Orchard, Bourne Road, Bilsington, Ashford, Kent
            "100062046273",  # TN263EH -> TN263BS : New Barn Farm, Ashford Road, High Halden, Ashford, Kent
            "100062567434",  # TN306SS -> TN306SP : Silver Oaks, Ashford Road, St Michaels, Tenterden, Kent
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "200004387668",  # TN257HH -> TN257DG : Mobile 1 Frithfield Farm, Frith Road, Aldington, Ashford, Kent
            "100062047443",  # TN270EP -> TN270QE : 2 Home Farm Cottages, Hurstford Lane, Little Chart, Ashford, Kent
            "100062047442",  # TN270EP -> TN270QE : 1 Home Farm Cottages, Hurstford Lane, Little Chart, Ashford, Kent
            "200004386965",  # TN257DQ -> TN257DG : Coach House, Pantile, Frith Road, Aldington, Ashford, Kent
            "100060799977",  # TN261HW -> TN261HL : 79 Tally Ho Road, Shadoxhurst, Ashford, Kent
            "200001798430",  # TN261LP -> TN261LR : Belantina, Woodchurch Road, Shadoxhurst, Ashford, Kent
        ]:
            rec["accept_suggestion"] = False

        return rec
