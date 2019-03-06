from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000212"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019Runny.tsv"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019Runny.tsv"
    elections = ["local.2019-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100061498464",  # TW200BJ -> TW200BQ : Chestnuts, Royal Holloway University - Halls of Residence, Englefield Green, Egham, Surrey
            "200001732773",  # TW208HJ -> TW200HJ : Brook Lodge, Wick Road, Englefield Green, Egham, Surrey
            "10002019662",  # KT153NT -> KT153QE : Accomodation at The Black Prince, Woodham Lane
            "100061503485",  # TW209UY -> TW209UX : Hogsters Farm, Stroude Road
            "100061499461",  # TW208LQ -> TW208QN : Rose Cottage, Green Road, Thorpe, Egham, Surrey
        ]:
            rec["accept_suggestion"] = True

        if uprn in []:
            rec["accept_suggestion"] = False

        return rec
