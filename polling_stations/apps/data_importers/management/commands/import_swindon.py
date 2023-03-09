from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SWD"
    addresses_name = (
        "2023-05-04/2023-03-09T15:11:04.745110/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-09T15:11:04.745110/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10090042967",  # 2 COMET WAY, WROUGHTON, SWINDON
            "200002920576",  # 549A CRICKLADE ROAD, SWINDON
            "10004837907",  # 47 VICTORIA ROAD, SWINDON
            "10004842282",  # 15B VICTORIA ROAD, SWINDON
            "10004837805",  # 15A VICTORIA ROAD, SWINDON
            "10009420836",  # HILLIER FUNERAL SERVICE LTD, KINGSHILL HOUSE, KENT ROAD, SWINDON
            "200001616306",  # ANDY WRAIGHT TEACHING STUDIOS, 105 RODBOURNE ROAD, SWINDON
            "10008541750",  # 1 BOUNDARY COTTAGES, WROUGHTON, SWINDON
            "10008541749",  # 2 BOUNDARY COTTAGES, WROUGHTON, SWINDON
        ]:
            return None

        if record.addressline6 in [
            # splits
            "SN25 3LR",
            "SN25 3EN",
            "SN6 7JY",
            "SN3 5EP",
            "SN25 2TN",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # The Nythe Centre, The Drive, Swindon, SN3 3RR
        if record.polling_place_id == "11659":
            record = record._replace(polling_place_postcode="SN3 3QA")

        return super().station_record_to_dict(record)
