from data_importers.ems_importers import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):

    council_id = "GRT"
    addresses_name = "2021-03-05T15:09:15.797593/polling_station_export-2021-03-05.csv"
    stations_name = "2021-03-05T15:09:15.797593/polling_station_export-2021-03-05.csv"
    elections = ["2021-05-06"]

    def address_record_to_dict(self, record):
        if record.housepostcode in ["GU1 1AD", "GU23 7JL"]:
            return None
        return super().address_record_to_dict(record)
