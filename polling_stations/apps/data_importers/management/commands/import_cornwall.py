from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CON"
    addresses_name = (
        "2024-05-02/2024-04-04T14:05:55.904632/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-04-04T14:05:55.904632/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Amendments from previous elections:

        # Methodist Sunday School Room Canworthy Water Launceston PL15 8UW
        if record.polling_place_id == "15105":
            record = record._replace(polling_place_uprn="10003300470")

        # The Cove Hall Wilcove Torpoint PL11 2PT
        if record.polling_place_id == "14619":
            record = record._replace(polling_place_uprn="10003065058")

        # St Austell Rugby Club Tregorrick Lane St Austell PL26 7FH
        if record.polling_place_id == "14259":
            record = record._replace(polling_place_uprn="10002694687")

        # Millbrook Village Hall The Parade Millbrook Torpoint
        if record.polling_place_id == "14757":
            record = record._replace(polling_place_uprn="10023432417")

        # Removing suspect postcode and coordinates

        # The Victory Hall St Francis Road Indian Queens St Columb TR9 6JR TR9 6JR
        if record.polling_place_id == "14315":
            record = record._replace(
                polling_place_postcode="",
            )
        # The Conference Room, Tregawn Farm, Michaelstow, Bodmin PL30 3PB
        if record.polling_place_id == "15166":
            record = record._replace(
                polling_place_easting="",
                polling_place_northing="",
            )
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")
        if uprn in [
            "10094078885",  # CARAVAN 5A GWINEAR DOWNS, LEEDSTOWN
            "10003919329",  # LOWER ORCHARD, ADIT LANE, SOUTH PILL, SALTASH
            "10002045559",  # THE ORCHARD, ADIT LANE, SOUTH PILL, SALTASH
        ]:
            return None
        if record.addressline6 in [
            # split
            "TR26 1EZ",
            "PL15 7BJ",
            "PL11 2HW",
            "TR27 4RZ",
            "TR27 4AG",
            "TR11 4PT",
            "TR26 2AQ",
            "PL18 9BJ",
            "TR19 6BH",
            "PL30 3DH",
            "TR8 4NR",
            "PL32 9UN",
            "TR16 5QD",
            "TR2 5JS",
            "TR20 8TG",
            "TR18 5NA",
            "PL15 8RF",
            "PL25 4EL",
            "TR18 3NH",
            "PL15 7SE",
            "PL31 2PB",
        ]:
            return None
        return super().address_record_to_dict(record)
