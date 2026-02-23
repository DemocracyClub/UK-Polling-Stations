from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "DND"
    addresses_name = "2026-05-07/2026-02-23T10:35:14.409147/Democracy Club - Idox_2026-02-20 13-27.csv"
    stations_name = "2026-05-07/2026-02-23T10:35:14.409147/Democracy Club - Idox_2026-02-20 13-27.csv"
    elections = ["2026-05-07"]

    def station_record_to_dict(self, record):
        # The following stations' postcodes have been verified by the council:
        # 'Wellgate Sheltered Housing, 8 King Street, Dundee, DD1 2JB' (id: 78)
        # 'Marryat Hall, City Square, Dundee, DD1 3BG' (id: 79)
        # 'Foula Terrace Sheltered, Housing Communal Lounge, Foula Terrace, Dundee, DD4 9SS' (id: 5)
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.postcode in [
            # split
            "DD2 1DJ",
            "DD3 6HW",
            "DD4 0TQ",
            "DD4 9ET",
            "DD1 1JS",
            "DD3 0JG",
            "DD4 6JU",
            "DD4 8RX",
            "DD4 0FD"
            # suspect
            "DD2 1RT",
        ]:
            return None
        return super().address_record_to_dict(record)
