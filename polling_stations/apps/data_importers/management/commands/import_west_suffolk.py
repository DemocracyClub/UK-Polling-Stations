from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WSK"
    addresses_name = (
        "2023-05-04/2023-03-13T16:10:41.345002/Democracy_Club__04May2023.CSV"
    )
    stations_name = (
        "2023-05-04/2023-03-13T16:10:41.345002/Democracy_Club__04May2023.CSV"
    )
    elections = ["2023-05-04"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100091029230",  # 23 BURY ROAD, NEWMARKET
            "200001370253",  # 27 BURY ROAD, NEWMARKET
        ]:
            return None
        return super().address_record_to_dict(record)
