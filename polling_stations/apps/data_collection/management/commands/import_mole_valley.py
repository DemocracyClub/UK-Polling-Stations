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
        if record.polling_place_id == "4260":  # Catholic Church Hall
            record = record._replace(polling_place_postcode="KT22 7EZ")

        # recieved from council
        if record.polling_place_id == "4231":  # Bookham Baptist Church Hall
            record = record._replace(
                polling_place_name="Bookham Baptist Church",
                polling_place_address_1="the Sanctuary",
                polling_place_address_2="Lower Road",
                polling_place_address_3="Bookham",
            )

        if record.polling_place_id == "4228":  # Bookham Scouting Centre
            record = record._replace(
                polling_place_address_1="Eastwick Park Avenue",
                polling_place_address_2="Bookham",
                polling_place_address_3="Surrey",
                polling_place_postcode="KT23 3NA",
            )

        if record.polling_place_id == "4213":  #  John Venus Hall, Coldharbour, RH5 6HF
            record = record._replace(
                polling_place_address_1="Coldharbour",
                polling_place_address_2="",
                polling_place_postcode="RH5 6HF",
            )
        if (
            record.polling_place_id == "4186"
        ):  #  Hookwood Memorial Hall, Withey Meadows, Hookwood, RH6 0AZ
            record = record._replace(polling_place_name="Hookwood Memorial Hall",)

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
