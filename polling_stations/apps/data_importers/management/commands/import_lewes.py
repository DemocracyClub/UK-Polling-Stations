from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "LEE"
    addresses_name = "2021-03-29T16:19:50.895276/polling_station_export-2021-03-24.csv"
    stations_name = "2021-03-29T16:19:50.895276/polling_station_export-2021-03-24.csv"
    elections = ["2021-05-06"]
    #
    def address_record_to_dict(self, record):

        if record.housepostcode in [
            "BN8 5NX" "RH17 7QH",
        ]:
            return None

        return super().address_record_to_dict(record)
