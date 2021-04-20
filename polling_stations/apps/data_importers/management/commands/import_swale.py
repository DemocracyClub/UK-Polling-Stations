from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "SWL"
    addresses_name = "2021-04-19T15:31:29.401515/polling_station_export-2021-03-02.csv"
    stations_name = "2021-04-19T15:31:29.401515/polling_station_export-2021-03-02.csv"
    elections = ["2021-05-06"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")
        if record.housepostcode in [
            "ME13 7NB",
            "ME10 2EF",
            "ME12 2HP",
            "ME12 2SG",
            "ME10 3TU",
            "ME12 1TF",
        ]:
            return None

        if uprn in [
            "200002533735",  # POPPINGTON BUNGALOW, WHITE HILL, SELLING, FAVERSHAM
            "200002536488",  # SIMEL HOUSE, MINTCHING WOOD LANE, KINGSDOWN, SITTINGBOURNE
        ]:
            return None

        return super().address_record_to_dict(record)
