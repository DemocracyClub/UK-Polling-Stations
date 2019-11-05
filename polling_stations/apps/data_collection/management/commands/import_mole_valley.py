from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000210"
    addresses_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019Mole.tsv"
    stations_name = "parl.2019-12-12/Version 1/Democracy_Club__12December2019Mole.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"
    allow_station_point_from_postcode = False

    def station_record_to_dict(self, record):
        # Carried over from local.2019-05-02 & europarl.2019-05-23
        if record.polling_place_id == "3742":  # Catholic Church Hall
            record = record._replace(polling_place_postcode="KT22 7EZ")
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in ["10010536066", "10010536270"]:
            return None

        if uprn in [
            "200000164356",  # RH42HQ -> RH41AY : 28/30 South Street, Dorking, Surrey
            "100062603678",  # RH41RU -> RH41AW : First Floor, 81 - 85 High Street, Dorking, Surrey
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "100061423632",  # RH56HJ -> RH54LR : The Reeds, Broome Hall, Coldharbour, Dorking, Surre
            "200000168944",  # RH55AF -> RH54RW : Caravan Henfold Lake Fisheries, Henfold Lane, Newdigate, Dorking, Surrey
            "200000168013",  # KT211AW -> RH60DS : 76A The Street, Ashtead, Surrey
        ]:
            rec["accept_suggestion"] = False

        return rec
