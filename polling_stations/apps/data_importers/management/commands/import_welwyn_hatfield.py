from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "WEW"
    addresses_name = (
        "2022-05-05/2022-04-08T11:34:35.289156/polling_station_export-2022-04-07.csv"
    )
    stations_name = (
        "2022-05-05/2022-04-08T11:34:35.289156/polling_station_export-2022-04-07.csv"
    )
    elections = ["2022-05-05"]

    # Checked the properties on Digswell Hill/Welwyn Bypass Road/Great North Road
    # and White Hill, and concluded they're fine, despite looking embedded in another area.
