from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "LDS"
    addresses_name = (
        "2022-05-05/2022-03-24T08:34:02.477217/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-24T08:34:02.477217/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "72132919",
            "72721195",
            "72546421",
            "72660575",
        ]:
            return None

        if record.addressline6 in [
            "LS12 2BN",
            "LS15 0LG",
            "LS14 6TS",
            "LS29 6FD",
            "LS10 4AZ",
            "LS25 1AX",
            "LS17 9ED",
            "LS10 4BD",
            "LS28 7HU",
            "WF3 2GL",
            "LS3 1BT",
            "LS18 5HN",
            "LS12 6DJ",
            "LS26 8TD",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # South Pudsey Community Education Training Centre,(Access via Lumby Lane), Pudsey
        if record.polling_place_id == "13693":
            record = record._replace(
                polling_place_easting="422971", polling_place_northing="432645"
            )
        # St Peters Church, (Worship Area), Hough Lane
        if record.polling_place_id == "13304":
            record = record._replace(
                polling_place_easting="424519", polling_place_northing="435050"
            )
        # Seacroft Community Hub, (Boardroom 1),  1 Seacroft Avenue
        if record.polling_place_id == "13575":
            record = record._replace(
                polling_place_easting="435693", polling_place_northing="436219"
            )

        # Corrections from council
        # Haigh Road Community Centre
        if record.polling_place_id == "13046":
            record = record._replace(
                polling_place_easting="434066", polling_place_northing="428893"
            )

        # New Travellers Rest
        if record.polling_place_id == "14341":
            record = record._replace(
                polling_place_name="Newman Centre",
                polling_place_address_1="(The Conference Room)",
                polling_place_address_2="Station Road",
                polling_place_address_4="Cross Gates",
                polling_place_postcode="LS15 7JY",
                polling_place_easting="436102",
                polling_place_northing="434587",
            )

        # Haigh Road Community Centre, Haigh Road LS26 0LW
        if record.polling_place_id == "13046":
            record = record._replace(polling_place_easting="434066")
            record = record._replace(polling_place_northing="428893")

        return super().station_record_to_dict(record)
