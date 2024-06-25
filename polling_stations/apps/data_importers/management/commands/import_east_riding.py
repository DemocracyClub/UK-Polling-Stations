from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "ERY"
    addresses_name = "2024-07-04/2024-06-25T14:39:04.816838/ERY_PD_combined.csv"
    stations_name = "2024-07-04/2024-06-25T14:39:04.816838/ERY_PS_combined.csv"
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10093602661",  # APARTMENT 26, ROGERSON COURT, SCAIFE GARTH, POCKLINGTON, YORK
            "10095588833",  # PROVENCE HOUSE, LAVENDER FIELDS, BARMBY MOOR, YORK
            "10093602661",  # APARTMENT 26, ROGERSON COURT, SCAIFE GARTH, POCKLINGTON, YORK
        ]:
            return None

        if record.postcode in [
            # splits
            "HU18 1EH",
            "HU10 7AD",
        ]:
            return None

        return super().address_record_to_dict(record)
