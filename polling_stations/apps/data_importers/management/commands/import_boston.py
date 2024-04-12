from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BOT"
    addresses_name = (
        "2024-05-02/2024-04-12T08:19:30.732163/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-04-12T08:19:30.732163/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200004473651",  # HARDEN CASTLE, KIRTON DROVE, KIRTON FEN, LINCOLN
            "200004471198",  # 3 WALNUT LODGE, WAINFLEET ROAD, BOSTON
        ]:
            return None

        if record.addressline6 in [
            # split
            "PE21 7AL",
            "PE21 8LA",
            "PE20 2BD",
            "PE21 0RL",
            "PE20 3ES",
            "PE22 9JW",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Holland Fen Parish Hall, Holland Fen, Lincoln
        if record.polling_place_id == "4589":
            record = record._replace(
                polling_place_postcode="LN4 4QH",
                polling_place_easting="523174",
                polling_place_northing="350120",
            )

        # Church Room Kirton Holme, Kirton Holme
        if record.polling_place_id == "4576":
            record = record._replace(
                polling_place_easting="526252",
                polling_place_northing="341966",
            )

        # Skirbeck St Nicholas Community Centre, Fishtoft Road, Boston, Lincs
        if record.polling_place_id == "4490":
            record = record._replace(
                polling_place_easting="533755",
                polling_place_northing="343209",
            )

        # Fenside Community Centre, Taverner Road, Boston
        if record.polling_place_id == "4471":
            record = record._replace(
                polling_place_easting="531820",
                polling_place_northing="344645",
            )

        # St Thomas Church Hall, London Road Boston,
        if record.polling_place_id == "4493":
            record = record._replace(
                polling_place_easting="532487",
                polling_place_northing="342724",
            )

        return super().station_record_to_dict(record)
