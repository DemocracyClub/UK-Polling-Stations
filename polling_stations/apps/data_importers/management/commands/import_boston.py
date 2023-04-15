from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BOT"
    addresses_name = (
        "2023-05-04/2023-04-13T15:06:11.607172/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-04-13T15:06:11.607172/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200004471896",  # FARM COTTAGE, IRELAND FARM, FREISTON INGS, BOSTON
        ]:
            return None

        if record.addressline6 in [
            "PE21 7BJ",
            "PE20 3ES",
            "PE21 0RL",
            "PE21 8LA",
            "PE21 7AL",
            "PE22 9JW",
            "PE21 7FN",
            "PE20 2BD",
            "PE20 1TG",  # KIRTON HOLME, BOSTON
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Holland Fen Parish Hall, Holland Fen, Lincoln
        if record.polling_place_id == "4309":
            record = record._replace(
                polling_place_postcode="LN4 4QH",
                polling_place_easting="523174",
                polling_place_northing="350120",
            )

        # Church Room Kirton Holme, Kirton Holme
        if record.polling_place_id == "4277":
            record = record._replace(
                polling_place_postcode="PE20 1SY",
                polling_place_easting="526252",
                polling_place_northing="341966",
            )

        # Skirbeck St Nicholas Community Centre, Fishtoft Road, Boston, Lincs
        if record.polling_place_id == "4288":
            record = record._replace(
                polling_place_postcode="PE21 0DL",
                polling_place_easting="533755",
                polling_place_northing="343209",
            )

        # Fenside Community Centre, Taverner Road, Boston
        if record.polling_place_id == "4338":
            record = record._replace(
                polling_place_postcode="PE21 8NL",
                polling_place_easting="531820",
                polling_place_northing="344645",
            )

        # St Thomas Church Hall, London Road Boston,
        if record.polling_place_id == "4236":
            record = record._replace(
                polling_place_easting="532487",
                polling_place_northing="342724",
            )

        return super().station_record_to_dict(record)
