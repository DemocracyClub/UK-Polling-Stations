from data_importers.ems_importers import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SWD"
    addresses_name = "2021-03-25T13:50:57.391940/Swindon Democracy_Club__06May2021.tsv"
    stations_name = "2021-03-25T13:50:57.391940/Swindon Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        if record.polling_place_id == "10577":
            # Central Community Centre Emlyn Square Entrance Railway Village Swindon
            record = record._replace(polling_place_postcode="SN1 5BP")
        if record.polling_place_id == "10369":
            # Nythe Community Centre The Drive Swindon
            record = record._replace(polling_place_postcode="SN3 3QA")
        if record.polling_place_id == "10329":
            # All Saints Church Southbrook Street Swindon
            record = record._replace(polling_place_postcode="SN2 1HF")
        if record.polling_place_id == "10357":
            # The Snooker Room The Tawny Owl Queen Elizabeth Drive Taw Hill Swindon
            record = record._replace(polling_place_postcode="SN25 1WR")
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10090042967",  # 2 COMET WAY, WROUGHTON, SWINDON
            "10009420836",  # KINGSHILL TRUST, KINGSHILL HOUSE, KENT ROAD, SWINDON
            "10094330068",  # FLAT 5, 103 COMMERCIAL ROAD, SWINDON
            "10094328819",  # 170A RODBOURNE ROAD, SWINDON
            "10010427210",  # 71 EASTBURY WAY, SWINDON
            "10010424377",  # 69 EASTBURY WAY, SWINDON
            "10010427209",  # 67 EASTBURY WAY, SWINDON
            "10010427208",  # 65 EASTBURY WAY, SWINDON
            "10010425158",  # 100 EASTBURY WAY, SWINDON
            "10010425157",  # 98 EASTBURY WAY, SWINDON
            "10010425156",  # 96 EASTBURY WAY, SWINDON
            "10010425159",  # 102 EASTBURY WAY, SWINDON
        ]:
            return None

        if record.addressline6 in [
            "SN25 1TX",
            "SN26 8BZ",
            "SN2 2AG",
            "SN25 3EN",
            "SN25 3LR",
            "SN1 3AS",
            "SN1 5QP",
            "SN3 2LQ",
            "SN3 5EP",
            "SN6 7JY",
            "SN25 2DZ",
            "SN6 7DG",
        ]:
            return None

        return super().address_record_to_dict(record)
