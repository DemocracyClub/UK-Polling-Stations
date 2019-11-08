from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000212"
    addresses_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019Runny.tsv"
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019Runny.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100061498464",  # TW200BJ -> TW200BQ : Chestnuts, Royal Holloway University - Halls of Residence, Englefield Green, Egham, Surrey
            "200001732773",  # TW208HJ -> TW200HJ : Brook Lodge, Wick Road, Englefield Green, Egham, Surrey
        ]:
            rec["accept_suggestion"] = True

        return rec
