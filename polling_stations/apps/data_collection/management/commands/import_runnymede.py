from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000212"
    addresses_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019runny.tsv"
    stations_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019runny.tsv"
    elections = ["europarl.2019-05-23"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100061498464",  # TW200BJ -> TW200BQ : Chestnuts, Royal Holloway University - Halls of Residence, Englefield Green, Egham, Surrey
            "200001732773",  # TW208HJ -> TW200HJ : Brook Lodge, Wick Road, Englefield Green, Egham, Surrey
            "10002019662",  # KT153NT -> KT153QE : Accomodation at The Black Prince, Woodham Lane
        ]:
            rec["accept_suggestion"] = True

        return rec
