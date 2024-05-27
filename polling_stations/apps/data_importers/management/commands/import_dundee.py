from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "DND"
    addresses_name = "2024-07-04/2024-05-28T10:15:27.215621/dundee_combined.csv"
    stations_name = "2024-07-04/2024-05-28T10:15:27.215621/dundee_combined.csv"
    elections = ["2024-07-04"]

    def station_record_to_dict(self, record):
        # 'Wellgate Sheltered Housing, 8 King Street, Dundee, DD1 2JB' (id: 78)
        if record.pollingvenueid == "78":
            record = record._replace(pollingstationpostcode="")

        # 'Marryat Hall, City Square, Dundee, DD1 3BG' (id: 79)
        if record.pollingvenueid == "79":
            record = record._replace(pollingstationpostcode="")

        # 'Foula Terrace Sheltered, Housing Communal Lounge, Foula Terrace, Dundee, DD4 9SS' (id: 5)
        if record.pollingvenueid == "5":
            record = record._replace(pollingstationpostcode="")
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            # split
            "DD4 0FD",
            "DD4 9ET",
            "DD4 6JU",
            "DD1 1JS",
            "DD4 0TQ",
            "DD4 8RX",
            "DD2 1DJ",
            "DD3 6AU",
            "DD2 2LR",
            "DD3 0JG",
            # suspect
            "DD2 1RT",
        ]:
            return None
        return super().address_record_to_dict(record)
