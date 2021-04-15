from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "DEB"
    addresses_name = (
        "2021-03-29T10:09:54.269326/Derbyshire Dales - Polling Districts Data.csv"
    )
    stations_name = (
        "2021-03-29T10:09:54.269326/Derbyshire Dales - Polling Station Data.csv"
    )
    elections = ["2021-05-06"]
