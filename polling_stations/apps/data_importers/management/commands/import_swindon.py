from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SWD"
    addresses_name = (
        "2024-07-04/2024-05-30T10:29:22.609055/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-05-30T10:29:22.609055/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200002920576",  # 549A CRICKLADE ROAD, SWINDON
            "10004837907",  # 47 VICTORIA ROAD, SWINDON
            "10004842282",  # 15B VICTORIA ROAD, SWINDON
            "10004837805",  # 15A VICTORIA ROAD, SWINDON
            "10009420836",  # HILLIER FUNERAL SERVICE LTD, KINGSHILL HOUSE, KENT ROAD, SWINDON
            "200001616306",  # ANDY WRAIGHT TEACHING STUDIOS, 105 RODBOURNE ROAD, SWINDON
            "200002926617",  # 14 LECHLADE ROAD, HIGHWORTH, SWINDON
            "200002926616",  # 13 LECHLADE ROAD, HIGHWORTH, SWINDON
            "10026656923",  # 12A 12 LECHLADE ROAD, HIGHWORTH, SWINDON
            "10010430974",  # 12 LECHLADE ROAD, HIGHWORTH, SWINDON
            "10022785691",  # 10 LECHLADE ROAD, HIGHWORTH, SWINDON
            "10008546617",  # INALA, LECHLADE ROAD, HIGHWORTH, SWINDON
            "10090044451",  # JOURNEYS END, LECHLADE ROAD, HIGHWORTH, SWINDON
            "10008546728",  # FOURWINDS, LECHLADE ROAD, HIGHWORTH, SWINDON
            "100121128471",  # ROYAL OAK, 24 DEVIZES ROAD, SWINDON
            "100121128472",  # 25 DEVIZES ROAD, SWINDON
            "10026656296",  # 29B SAVERNAKE STREET, SWINDON
            "10026656295",  # 29A SAVERNAKE STREET, SWINDON
            "10004845458",  # FLAT 16 VICTORIA ROAD, OLD TOWN, SWINDON
            "200002920837",  # 597 CRICKLADE ROAD, SWINDON
            "10090041392",  # 340A CRICKLADE ROAD, SWINDON
            "10004837797",  # 26 VICTORIA ROAD, SWINDON
            "200001618187",  # 198 MARLBOROUGH ROAD, SWINDON
            "100121169159",  # THE BUNGALOW, DORCAN COMPREHENSIVE SCHOOL, ST. PAULS DRIVE, DORCAN, SWINDON
        ]:
            return None

        if record.addressline6 in [
            # splits
            "SN25 3LR",
            "SN6 7JY",
            "SN25 2TN",
            # looks wrong
            "SN6 7DG",
            "SN1 3FP",
        ]:
            return None

        return super().address_record_to_dict(record)
