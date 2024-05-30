from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BOT"
    addresses_name = (
        "2024-07-04/2024-05-30T16:36:53.343765/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-05-30T16:36:53.343765/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200004473651",  # HARDEN CASTLE, KIRTON DROVE, KIRTON FEN, LINCOLN
            "200004471198",  # 3 WALNUT LODGE, WAINFLEET ROAD, BOSTON
            "200004471896",  # FARM COTTAGE, IRELAND FARM, FREISTON INGS, BOSTON
            "200001828505",  # HIDEAWAY COTTAGE, HAMPTON LANE, OLD LEAKE, BOSTON
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
        if record.polling_place_id == "4805":
            record = record._replace(
                polling_place_postcode="LN4 4QH",
                polling_place_easting="523174",
                polling_place_northing="350120",
            )

        # Church Room Kirton Holme, Kirton Holme
        if record.polling_place_id == "4790":
            record = record._replace(
                polling_place_easting="526252",
                polling_place_northing="341966",
            )

        # Skirbeck St Nicholas Community Centre, Fishtoft Road, Boston, Lincs
        if record.polling_place_id == "4701":
            record = record._replace(
                polling_place_easting="533755",
                polling_place_northing="343209",
            )

        # Fenside Community Centre, Taverner Road, Boston
        if record.polling_place_id == "4682":
            record = record._replace(
                polling_place_easting="531820",
                polling_place_northing="344645",
            )

        # St Thomas Church Hall, London Road Boston,
        if record.polling_place_id == "4705":
            record = record._replace(
                polling_place_easting="532487",
                polling_place_northing="342724",
            )

        return super().station_record_to_dict(record)
