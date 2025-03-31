from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "PTE"
    addresses_name = (
        "2025-05-01/2025-03-31T16:53:28.554952/Democracy_Club__01May2025.CSV"
    )
    stations_name = (
        "2025-05-01/2025-03-31T16:53:28.554952/Democracy_Club__01May2025.CSV"
    )
    elections = ["2025-05-01"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10094542529",  # 64 GREENFIELD WAY, HAMPTON WATER, PETERBOROUGH
            "100091206701",  # WOODLANDS, HAM LANE, ORTON WATERVILLE, PETERBOROUGH
            "10090764144",  # 43B SILVERWOOD ROAD, MILLFIELD, PETERBOROUGH
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Below warnings checked and no correction needed:
        # Polling station Wothorpe Sports Centre (11397) is in South Kesteven District Council (SKE)
        return super().station_record_to_dict(record)
