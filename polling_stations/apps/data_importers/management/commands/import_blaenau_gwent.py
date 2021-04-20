from data_importers.ems_importers import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):

    council_id = "BGW"
    addresses_name = (
        "2021-03-29T15:39:51.593346/Blaenau Gwent polling_station_export-2021-03-29.csv"
    )
    stations_name = (
        "2021-03-29T15:39:51.593346/Blaenau Gwent polling_station_export-2021-03-29.csv"
    )
    elections = ["2021-05-06"]
    csv_encoding = "windows-1252"

    def station_record_to_dict(self, record):
        # EBENEZER CHAPEL VESTRY
        if record.pollingstationnumber in [
            "62",  # EBENEZER CHAPEL VESTRY
            "54",  # SCOUT HUT, VICTOR ROAD
            "25",  # ST. JOHN’S AMBULANCE HALL
        ]:
            record = record._replace(pollingstationpostcode="")
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):

        if record.housepostcode in ["NP23 5DH", "NP13 3AQ"]:
            return None

        return super().address_record_to_dict(record)
