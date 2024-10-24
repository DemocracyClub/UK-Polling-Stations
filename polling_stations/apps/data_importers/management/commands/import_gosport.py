from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "GOS"
    addresses_name = "2024-11-21/2024-10-24T13:53:59.874871/2024 LGBE - Democracy Club Polling Districts v1.csv"
    stations_name = "2024-11-21/2024-10-24T13:53:59.874871/2024 LGBE - Democracy Club Polling Stations v1.csv"
    elections = ["2024-11-21"]
    csv_encoding = "utf-16le"

    # Preserving the postcode exclusions for reference during the next local elections

    # def address_record_to_dict(self, record):
    #     if record.postcode in [
    #         # suspect
    #         "PO12 1SE",
    #         "PO12 4AW",
    #         "PO12 4QE",
    #         "PO12 4JP",
    #     ]:
    #         return None

    #     return super().address_record_to_dict(record)
