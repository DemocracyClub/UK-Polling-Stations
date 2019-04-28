from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000210"
    addresses_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019Mole.tsv"
    stations_name = "local.2019-05-02/Version 1/Democracy_Club__02May2019Mole.tsv"
    elections = ["local.2019-05-02"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):

        if record.polling_place_id == "3476":
            record = record._replace(polling_place_postcode="KT22 7PR")

        if record.polling_place_id == "3479":
            record = record._replace(polling_place_postcode="KT22 7EZ")

        if record.polling_place_id == "3382":
            record = record._replace(polling_place_postcode="KT22 4AQ")

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
