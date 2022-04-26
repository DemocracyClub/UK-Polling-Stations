from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HRY"
    addresses_name = (
        "2022-05-05/2022-02-24T11:12:13.458448/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-02-24T11:12:13.458448/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        if record.polling_place_id in (
            "9027",  # St Michael`s CE Primary School N6 4BG
            "9149",  # The Scout Hall, All Hallows Road, N17 7AD
            "9062",  # Calvary Church Hall, N17 0TB
            "9000",  # St Andrew`s Centre
        ):
            record = record._replace(polling_place_easting="0")
            record = record._replace(polling_place_northing="0")

        # St Marys CE Primary School
        if record.polling_place_id == "9043":
            record = record._replace(polling_place_postcode="N8 7BU")
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if record.addressline6 in [
            "N15 5NP",
            "N17 8HF",
            "N6 5UE",
            "N15 3RA",
            "N15 3QB",
            "N22 8ET",
            "N15 6DL",
            "N15 3LX",
        ]:
            return None

        if uprn in [
            "100021190559",  # 107 HIGH ROAD, LONDON
            "100021236685",  # FIRST FLOOR FLAT 24 WEST GREEN ROAD, TOTTENHAM, LONDON
            "100021236879",  # GROUND FLOOR FLAT 186 WEST GREEN ROAD, TOTTENHAM, LONDON
            "100021236940",  # FIRST FLOOR FLAT 294 WEST GREEN ROAD, TOTTENHAM, LONDON
            "100021236969",  # 333B WEST GREEN ROAD, TOTTENHAM, LONDON
            "10022936454",  # FLAT A 489 SEVEN SISTERS ROAD, TOTTENHAM, LONDON
            "10022936455",  # FLAT B 489 SEVEN SISTERS ROAD, TOTTENHAM, LONDON
            "10093592074",  # FLAT 1 1A WARGRAVE AVENUE, TOTTENHAM, LONDON
            "200002207397",  # FLAT A 39 ABBOTSFORD AVENUE, TOTTENHAM, LONDON
        ]:
            return None

        return super().address_record_to_dict(record)
