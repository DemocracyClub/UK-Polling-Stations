from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MOL"
    addresses_name = (
        "2023-05-04/2023-03-09T15:06:43.238353/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-09T15:06:43.238353/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Fairfield Centre - council address correction
        if record.polling_place_id == "5488":
            record = record._replace(
                polling_place_address_1="34 Swan Court",
                polling_place_address_2="High Street",
                polling_place_address_3="Leatherhead",
                polling_place_address_4="Surrey",
                polling_place_postcode="KT22 8AH",
            )
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200000162928",  # 2 BLACKBROOK FARM COTTAGES, BLACKBROOK ROAD, DORKING
            "200000162927",  # 1 BLACKBROOK FARM COTTAGES, BLACKBROOK ROAD, DORKING
            "100061426266",  # 5 RIDGEWAY CLOSE, DORKING
            "10000829965",  # 2 STABLE COTTAGE RUSPER ROAD, CAPEL
            "10000829964",  # 1 STABLE COTTAGE RUSPER ROAD, CAPEL
            "10000828494",  # ARNWOOD FARM COTTAGE RUSPER ROAD, NEWDIGATE
        ]:
            return None

        if record.addressline6 in ["RH5 4QY", "KT21 2LY"]:  # splits
            return None

        return super().address_record_to_dict(record)
