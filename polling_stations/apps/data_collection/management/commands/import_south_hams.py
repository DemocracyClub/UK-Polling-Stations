from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000044"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019Ham.tsv"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019Ham.tsv"
    elections = ["local.2019-05-02", "europarl.2019-05-23"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10008919576",  # TQ73JQ -> TQ73JG : Brook Mead, South Milton, Kingsbridge, Devon
            "10008915892",  # PL75BD -> PL75DB : The Vicarage, Sparkwell, Plymouth, Devon
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "10093769557",  # TQ96GU -> TQ96LB : Flat 1, 1 Jacks Close, Totnes, Devon
            "10093769558",  # TQ96GU -> TQ96LB : Flat 2, 1 Jacks Close, Totnes, Devon
            "10093769559",  # TQ96GU -> TQ96LB : Flat 3, 1 Jacks Close, Totnes, Devon
            "10093769560",  # TQ96GU -> TQ96LB : Flat 4, 1 Jacks Close, Totnes, Devon
            "10093769561",  # TQ96GU -> TQ96LB : Flat 5, 1 Jacks Close, Totnes, Devon
            "10093769562",  # TQ96GU -> TQ96LB : Flat 6, 1 Jacks Close, Totnes, Devon
            "10093769563",  # TQ96GU -> TQ96LB : Flat 7, 1 Jacks Close, Totnes, Devon
            "10093769564",  # TQ96GU -> TQ96LB : Flat 8, 1 Jacks Close, Totnes, Devon
            "10008919478",  # PL82LB -> PL82DN : Wood Cottage, Efford Farm, Yealmpton, Plymouth, Devon
            "10008914498",  # TQ72BT -> TQ88PW : Vinivers, East Prawle, Kingsbridge, Devon
            "10008922047",  # PL219NX -> PL219NU : The Laundry Cottage, Flete, Ivybridge, Devon
            "100040286599",  # TQ74AS -> TQ74AZ : Mirimar, Marine Drive, Bigbury-on-Sea, Kingsbridge, Devon
        ]:
            rec["accept_suggestion"] = False

        if record.addressline6 == "TQ11 0FA":
            return None

        return rec
