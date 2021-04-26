from django.contrib.gis.geos import Point
from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MDE"
    addresses_name = (
        "2021-04-16T11:24:22.888592/Mid Devon Democracy_Club__06May2021.tsv"
    )
    stations_name = "2021-04-16T11:24:22.888592/Mid Devon Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def station_record_to_dict(self, record):

        if record.polling_place_id in [
            "8700",  # Cullompton Town Hall, High Street, Cullompton EX15 1AB
            "8634",  # Chawleigh Jubilee Hall, Chawleigh EX18 7HH
            "8628",  # Thorverton Memorial Hall, Silver Street, Thorverton EX5 5LT
            "8615",  # Shobrooke Village Hall, Shobrooke EX17 1AT
            "8583",  # Crediton Congregational Church, High Street, Crediton EX17 3LB
        ]:
            record = record._replace(polling_place_easting="")
            record = record._replace(polling_place_northing="")

        # Crediton United Football Club Lords Meadow Sports Centre Commercial Road Crediton EX17 IER
        if record.polling_place_id == "8850":
            record = record._replace(polling_place_postcode="EX17 1ER")

        rec = super().station_record_to_dict(record)

        # Oakford Village Hall, Oakford EX16 9EW
        if record.polling_place_id == "8742":
            rec["location"] = Point(-3.550351, 50.982061, srid=4326)

        return rec

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10024639781",  # FOXHOLES FARM, CLAYHIDON, CULLOMPTON
            "10093536858",  # MOBILE HOME THE OLD OAKS CHAPEL HILL, UFFCULME
            "10035356543",  # THE OLD OAKS, CHAPEL HILL, UFFCULME, CULLOMPTON
            "10002162361",  # POTTERS, SHILLINGFORD, TIVERTON
            "10093536511",  # RAMSTORLAND STAG VIEW, STOODLEIGH, TIVERTON
            "200004004367",  # CARAVANS 3 AND 4 THREE ACRES UFFCULME ROAD, WILLAND
            "200004004366",  # CARAVANS 1 AND 2 THREE ACRES UFFCULME ROAD, WILLAND
            "10009446166",  # DYERS, BICKLEIGH, TIVERTON
            "200004001948",  # BACKSWOOD FARM, BICKLEIGH, TIVERTON
            "200004001949",  # BACKSWOOD FARM COTTAGE LANE TO BACKSWOOD FARM, BICKLEIGH
            "100040361739",  # FLAT 1 10 BRIDGE STREET, TIVERTON
            "10093534226",  # FLAT 2 10 BRIDGE STREET, TIVERTON
            "10002162357",  # RADDS COTTAGE, CALVERLEIGH, TIVERTON
            "200004002192",  # PRIMROSE LODGE, LOXBEARE, TIVERTON
            "10024639061",  # THE BIRDHOUSE, TEMPLETON, TIVERTON
            "10009448630",  # MAYFIELD HOUSE, TEMPLETON, TIVERTON
            "10002165647",  # POUND CASTLE, BICKLEIGH, TIVERTON
            "200004005422",  # GUNSTONE LODGE GUNSTONE PARK ROAD FROM GUNSTONE CROSS TO GUNSTONE MILL CROSS, GUNSTONE
            "200004006381",  # GUNSTONE PARK, GUNSTONE, CREDITON
            "10093533623",  # RAVENS WOOD, YEOFORD, CREDITON
            "200004002829",  # POND VIEW, UFFCULME, CULLOMPTON
        ]:
            return None

        if record.addressline6 in [
            "EX16 7RW",
        ]:
            return None

        return super().address_record_to_dict(record)
