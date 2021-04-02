from data_importers.ems_importers import BaseHalaroseCsvImporter

CLK_ADMINAREAS = (
    "Alloa",
    "Alva",
    "Clackmannan",
    "Clackmannanshire Ward 1",
    "Clackmannanshire Ward 2",
    "Clackmannanshire Ward 3",
    "Clackmannanshire Ward 4",
    "Clackmannanshire Ward 5",
    "Dollar",
    "Menstrie",
    "Tillicoultry",
)


class Command(BaseHalaroseCsvImporter):
    council_id = "CLK"
    addresses_name = "2021-04-01T20:38:39.906716/Central Scotland polling_station_export-2021-03-31.csv"
    stations_name = "2021-04-01T20:38:39.906716/Central Scotland polling_station_export-2021-03-31.csv"
    elections = ["2021-05-06"]

    def station_record_to_dict(self, record):
        if record.adminarea not in CLK_ADMINAREAS:
            return None

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.adminarea not in CLK_ADMINAREAS:
            return None

        return super().address_record_to_dict(record)
