from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "GRE"
    addresses_name = "2021-04-12T08:58:49.743842/polling_station_export-2021-04-11.csv"
    stations_name = "2021-04-12T08:58:49.743842/polling_station_export-2021-04-11.csv"
    elections = ["2021-05-06"]
    csv_delimiter = ","
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10010199305",  # 4-5 HILLREACH, LONDON
            "10010240758",  # 5 OGILBY STREET, LONDON
            "10010240756",  # 1 OGILBY STREET, LONDON
            "10010240757",  # 3 OGILBY STREET, LONDON
            "100020974501",  # 102A HERBERT ROAD, LONDON
            "100020980261",  # 67 KINGSLEY WOOD DRIVE, LONDON
            "100020989060",  # 209 MOORDOWN, LONDON
            "10010227617",  # 292B PLUMSTEAD COMMON ROAD, PLUMSTEAD
            "100020940599",  # 132 BEXLEY ROAD, LONDON
        ]:
            return None

        if record.housepostcode in ["SE9 6SQ", "SE9 2BU", "SE10 0PR", "SE10 8GS"]:
            return None

        return super().address_record_to_dict(record)
