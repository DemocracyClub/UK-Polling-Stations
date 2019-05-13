from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000210"
    addresses_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019.tsv"
    stations_name = "europarl.2019-05-23/Version 1/Democracy_Club__23May2019.tsv"
    elections = ["europarl.2019-05-23"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Carried over from local.2019-05-02
        if record.polling_place_id == "3742":  # Catholic Church Hall
            record = record._replace(polling_place_postcode="KT22 7EZ")
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200000164356"  # RH42HQ -> RH41AY : 28/30 South Street, Dorking, Surrey
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "100061423632",  # RH56HJ -> RH54LR : The Reeds, Broome Hall, Coldharbour, Dorking, Surre
            "200000168944",  # RH55AF -> RH54RW : Caravan Henfold Lake Fisheries, Henfold Lane, Newdigate, Dorking, Surrey
        ]:
            rec["accept_suggestion"] = False

        return rec
