from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "BGW"
    addresses_name = (
        "2022-05-05/2022-03-21T12:39:42.933221/polling_station_export-2022-03-21.csv"
    )
    stations_name = (
        "2022-05-05/2022-03-21T12:39:42.933221/polling_station_export-2022-03-21.csv"
    )
    elections = ["2022-05-05"]
    csv_encoding = "windows-1252"

    def station_record_to_dict(self, record):
        if record.pollingstationnumber in [
            "61",  # EBENEZER CHAPEL VESTRY
        ]:
            record = record._replace(pollingstationpostcode="NP22 4RQ")
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):

        if record.housepostcode in [
            "NP23 5DH",
            "NP13 3JU",
            "NP13 3AQ",
        ]:
            return None

        return super().address_record_to_dict(record)
