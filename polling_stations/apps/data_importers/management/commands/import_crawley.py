from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CRW"
    addresses_name = (
        "2024-07-04/2024-05-28T15:07:15.444005/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-05-28T15:07:15.444005/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100061788135",  # 79 PUNCH COPSE ROAD, CRAWLEY
            "100061767151",  # OAK COTTAGE, BALCOMBE ROAD, CRAWLEY
            "200001244362",  # PREMIER INN, CRAWLEY AVENUE, CRAWLEY
        ]:
            return None

        return super().address_record_to_dict(record)
