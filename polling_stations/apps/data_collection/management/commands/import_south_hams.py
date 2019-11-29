from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000044"
    addresses_name = "parl.2019-12-12/Version 1/merged.tsv"
    stations_name = "parl.2019-12-12/Version 1/merged.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if record.addressline6 in [
            "PL21 0SF",
            "TQ11 0FA",
        ]:
            return None

        if uprn in [
            "10090533923",
            "10009314953",
            "100040286136",
        ]:
            return None

        if uprn in [
            "10008919576",  # TQ73JQ -> TQ73JG : Brook Mead, South Milton, Kingsbridge, Devon
            "10008915892",  # PL75BD -> PL75DB : The Vicarage, Sparkwell, Plymouth, Devon
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "10008919478",  # PL82LB -> PL82DN : Wood Cottage, Efford Farm, Yealmpton, Plymouth, Devon
            "10008914498",  # TQ72BT -> TQ88PW : Vinivers, East Prawle, Kingsbridge, Devon
            "10008922047",  # PL219NX -> PL219NU : The Laundry Cottage, Flete, Ivybridge, Devon
            "100040286599",  # TQ74AS -> TQ74AZ : Mirimar, Marine Drive, Bigbury-on-Sea, Kingsbridge, Devon
        ]:
            rec["accept_suggestion"] = False

        return rec
