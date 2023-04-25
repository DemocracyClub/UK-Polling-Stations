from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "ERY"
    addresses_name = "2023-05-04/2023-04-25T18:30:43.685241/Democracy Club - LOCAL polling districts 2023.csv"
    stations_name = "2023-05-04/2023-04-25T18:30:43.685241/Democracy Club - LOCAL polling stations 2023.csv"
    elections = ["2023-05-04"]

    def address_record_to_dict(self, record):
        if record.postcode in [
            # split
            "HU18 1EH",
        ]:
            return None

        return super().address_record_to_dict(record)
