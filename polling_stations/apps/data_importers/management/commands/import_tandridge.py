from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "TAN"
    addresses_name = (
        "2022-05-05/2022-03-17T15:54:54.749645/polling_station_export-2022-03-17.csv"
    )
    stations_name = (
        "2022-05-05/2022-03-17T15:54:54.749645/polling_station_export-2022-03-17.csv"
    )
    elections = ["2022-05-05"]

    # For some reason the export only has these fields for station address
    station_address_fields = [
        "pollingstationname",
        "pollingstationaddress_1",
        "pollingstationaddress_2",
        "pollingstationaddress_3",
    ]

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            "CR3 6HG",
            "RH7 6JH",
        ]:
            return None

        return super().address_record_to_dict(record)
