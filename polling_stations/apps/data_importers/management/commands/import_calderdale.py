from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CLD"
    addresses_name = "2026-05-07/2026-03-17T16:40:35.655763/20260317_Democracy_Club__07May2026_CMBC.CSV"
    stations_name = "2026-05-07/2026-03-17T16:40:35.655763/20260317_Democracy_Club__07May2026_CMBC.CSV"
    elections = ["2026-05-07"]
    csv_encoding = "windows-1252"

    def station_record_to_dict(self, record):
        # # The following are coord amendments from the council:

        # PELLON BAPTIST SUNDAY SCHOOL, SPRING HALL LANE, HALIFAX, HX1 4UA
        if record.polling_place_id == "1310":
            record = record._replace(
                polling_place_easting="407498",
                polling_place_northing="425770",
            )

        # coord tweaks at the behest of the council to fix pathing issues:
        # All Saints Parish Hall Godfrey Road Halifax
        if record.polling_place_id == "1304":
            record = record._replace(
                polling_place_easting="409169",
                polling_place_northing="422981",
            )
        # Beechwood Library Beechwood Road Halifax West Yorkshire
        if record.polling_place_id == "1173":
            record = record._replace(
                polling_place_easting="407669",
                polling_place_northing="427825",
            )
        # Bethesda Methodist Church Victoria Road Elland
        if record.polling_place_id == "1064":
            record = record._replace(
                polling_place_easting="410601",
                polling_place_northing="420789",
            )
        # Boothtown Methodist Church Hall 39 Boothtown Road Halifax
        if record.polling_place_id == "1241":
            record = record._replace(
                polling_place_easting="408950",
                polling_place_northing="426445",
            )
        # Children`s Corner Preschool St Hilda`s Church Gibraltar Road Halifax
        if record.polling_place_id == "1190":
            record = record._replace(
                polling_place_easting="407371",
                polling_place_northing="424897",
            )
        # Cornholme & Portsmouth Old Library 1 Parkside Road Todmorden
        if record.polling_place_id == "1280":
            record = record._replace(
                polling_place_easting="390725",
                polling_place_northing="426318",
            )
        # Fielden Centre Ewood Lane Todmorden
        if record.polling_place_id == "1274":
            record = record._replace(
                polling_place_easting="392941",
                polling_place_northing="424910",
            )
        # Greetland Academy KS1 Saddleworth Road Greetland Halifax
        if record.polling_place_id == "1076":
            record = record._replace(
                polling_place_easting="408794",
                polling_place_northing="421019",
            )
        # Halifax Fire Station The Community Room Skircoat Moor Road Halifax West Yorkshire
        if record.polling_place_id == "1330":
            record = record._replace(
                polling_place_easting="407880",
                polling_place_northing="424116",
            )
        # Halifax Vandals RUFC Warley Town Lane Warley Halifax
        if record.polling_place_id == "1326":
            record = record._replace(
                polling_place_easting="405294",
                polling_place_northing="425078",
            )
        # Illingworth St Mary`s Cricket Club The Ainleys Alloe Field View Illingworth Halifax
        if record.polling_place_id == "1109":
            record = record._replace(
                polling_place_easting="407434",
                polling_place_northing="428738",
            )
        # St Andrew`s Methodist Church The Moore Hall Huddersfield Road Halifax
        if record.polling_place_id == "1307":
            record = record._replace(
                polling_place_easting="409563",
                polling_place_northing="423364",
            )
        # St Jude`s Church Hall Free School Lane Halifax
        if record.polling_place_id == "1340":
            record = record._replace(
                polling_place_easting="408710",
                polling_place_northing="424059",
            )
        # St Paul`s Church Parish Room Queens Road Halifax
        if record.polling_place_id == "1180":
            record = record._replace(
                polling_place_easting="407996",
                polling_place_northing="424459",
            )
        # Town Hall, Hebden Bridge St Georges Street Hebden Bridge
        if record.polling_place_id == "1031":
            record = record._replace(
                polling_place_easting="399240",
                polling_place_northing="427353",
            )

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.addressline6.replace("\xa0", " ") in [
            # split
            "HX3 8FY",
            # suspect
            "HX2 0UW",
        ]:
            return None

        return super().address_record_to_dict(record)
