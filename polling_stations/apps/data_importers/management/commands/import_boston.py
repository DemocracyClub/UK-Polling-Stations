from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BOT"
    addresses_name = (
        "2025-05-01/2025-03-03T10:27:16.115283/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-03T10:27:16.115283/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200004471896",  # FARM COTTAGE, IRELAND FARM, FREISTON INGS, BOSTON
            "200001828505",  # HIDEAWAY COTTAGE, HAMPTON LANE, OLD LEAKE, BOSTON
        ]:
            return None

        if record.addressline6 in [
            # split
            "PE20 3ES",
            "PE21 7AL",
            "PE21 8LA",
            "PE21 0RL",
            "PE20 2BD",
            "PE22 9JW",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Holland Fen Parish Hall, Holland Fen, Lincoln
        if record.polling_place_id == "5081":
            record = record._replace(
                polling_place_postcode="LN4 4QH",
                polling_place_easting="523174",
                polling_place_northing="350120",
            )

        # Church Room Kirton Holme, Kirton Holme
        if record.polling_place_id == "4979":
            record = record._replace(
                polling_place_easting="526252",
                polling_place_northing="341966",
            )

        # Skirbeck St Nicholas Community Centre, Fishtoft Road, Boston, Lincs
        if record.polling_place_id == "5050":
            record = record._replace(
                polling_place_easting="533755",
                polling_place_northing="343209",
            )

        # Fenside Community Centre, Taverner Road, Boston
        if record.polling_place_id == "5109":
            record = record._replace(
                polling_place_easting="531820",
                polling_place_northing="344645",
            )

        # St Thomas Church Hall, London Road Boston,
        if record.polling_place_id == "4964":
            record = record._replace(
                polling_place_easting="532487",
                polling_place_northing="342724",
            )

        return super().station_record_to_dict(record)
