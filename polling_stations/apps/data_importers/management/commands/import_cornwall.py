from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CON"
    addresses_name = (
        "2024-07-04/2024-06-20T12:34:38.090059/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-20T12:34:38.090059/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Amendments from previous elections:

        # Methodist Sunday School Room Canworthy Water Launceston PL15 8UW
        if record.polling_place_id == "16273":
            record = record._replace(polling_place_uprn="10003300470")

        # The Cove Hall Wilcove Torpoint PL11 2PT
        if record.polling_place_id == "15768":
            record = record._replace(polling_place_uprn="10003065058")

        # St Austell Rugby Club Tregorrick Lane St Austell PL26 7FH
        if record.polling_place_id == "16494":
            record = record._replace(polling_place_uprn="10002694687")

        # Millbrook Village Hall The Parade Millbrook Torpoint
        if record.polling_place_id == "15911":
            record = record._replace(polling_place_uprn="10023432417")

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
            "TR11 4PT",
            "PL11 2HW",
            "TR26 1EZ",
            "PL15 7BJ",
            "TR27 4AG",
            "TR18 5NA",
            "TR27 4RZ",
            "TR8 4NR",
            "TR26 2AQ",
            "PL32 9UN",
            "TR16 5QD",
            "PL15 7SE",
            "PL18 9BJ",
            "PL30 3DH",
            "TR19 6BH",
            "PL25 4EL",
            "TR20 8TG",
            "PL15 8RF",
            "TR2 5JS",
            "TR18 3NH",
            "PL31 2PB",
        ]:
            return None
        return super().address_record_to_dict(record)
