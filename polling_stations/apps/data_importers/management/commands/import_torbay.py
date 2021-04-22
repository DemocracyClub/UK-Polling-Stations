from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "TOB"
    addresses_name = "2021-04-09T11:31:36.785601/Democracy_Club__06May2021.tsv"
    stations_name = "2021-04-09T11:31:36.785601/Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def station_record_to_dict(self, record):

        # Central Garage Showroom Milton Street Brixham TQ5 OBY
        if record.polling_place_id == "8248":
            record = record._replace(polling_place_postcode="TQ5 0BX")

        # Paignton SNU Spiritualist Church Hall Manor Corner Torquay Road Paignton TQ3 1JB
        if record.polling_place_id == "8230":
            record = record._replace(polling_place_postcode="TQ3 2JB")

        # St Annes Hall Babbacombe Road Torquay TQ1 3UH
        if record.polling_place_id == "8242":
            record = record._replace(polling_place_postcode="")

        rec = super().station_record_to_dict(record)

        # Mobile Station at DFS Car Park Willows Retail Park Nicholson Road Torquay TQ2 7TD
        if record.polling_place_id == "8181":
            rec["location"] = Point(-3.556830, 50.488924, srid=4326)

        return rec

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10024001656",  # GATEHOUSE COTTAGE MUDSTONE LANE, BRIXHAM
            "100040534883",  # ZOO AND GARDENS NORTH LODGE TOTNES ROAD, PAIGNTON
            "10094527880",  # 140A TOTNES ROAD, PAIGNTON
            "100040529632",  # 16 OLD TORQUAY ROAD, PAIGNTON
            "100040526403",  # SMALLCOMBE, KINGS ASH ROAD, PAIGNTON
            "10093142379",  # 73A BLATCHCOMBE ROAD, PAIGNTON
            "10024003083",  # 30 SHORTON ROAD, PAIGNTON
            "100040532454",  # 28 SHORTON ROAD, PAIGNTON
            "10094526711",  # BARWOOD MEWS LOWER WARBERRY ROAD, TORQUAY
            "100041187053",  # TREETOPS, LOWER WARBERRY ROAD, TORQUAY
            "100040548856",  # FLAT 7, WARBERRY HOUSE, LOWER WARBERRY ROAD, TORQUAY
            "100040548855",  # FLAT 6, WARBERRY HOUSE, LOWER WARBERRY ROAD, TORQUAY
            "100040548852",  # FLAT 1, WARBERRY HOUSE, LOWER WARBERRY ROAD, TORQUAY
            "100040548854",  # FLAT 5, WARBERRY HOUSE, LOWER WARBERRY ROAD, TORQUAY
            "100040539413",  # FLAT A, CLIFTON HOUSE, BRADDONS HILL ROAD EAST, TORQUAY
            "100040539414",  # FLAT B, CLIFTON HOUSE, BRADDONS HILL ROAD EAST, TORQUAY
            "10094527881",  # THE MEADOWS, AVENUE ROAD, TORQUAY
            "10093141340",  # FLAT 2 ODDICOMBE HALL BABBACOMBE DOWNS ROAD, ST MARYCHURCH, TORQUAY
            "100040538743",  # DOWNSVIEW CORNER, BEDFORD ROAD, TORQUAY
            "10002985724",  # 8B ST. PAULS ROAD, TORQUAY
            "100040547447",  # 42 ISAACS ROAD, TORQUAY
            "100040541253",  # CHERRY BLOSSOM FARM, CLADDON LANE, MAIDENCOMBE, TORQUAY
            "100041198763",  # 308 DARTMOUTH ROAD, PAIGNTON
            "200002083269",  # PONTOON ADJ PRINCESS PIER, PONTOON ADJ PRINCESS PIER TORBAY ROAD, TORQUAY
            "100041200459",  # HOMELANDS, BERRY HEAD ROAD, BRIXHAM
            "100040513373",  # JESMOND COTTAGE MILTON STREET, BRIXHAM
            "100040519265",  # SUNNYBANK BRIXHAM ROAD, PAIGNTON
            "100040520900",  # THE MANSE CLIFTON ROAD, PAIGNTON
            "100041189794",  # THE OLD DAIRY, TEIGNMOUTH ROAD, MAIDENCOMBE, TORQUAY
        ]:
            return None

        if record.addressline6 in ["TQ1 4QZ"]:
            return None

        return super().address_record_to_dict(record)
