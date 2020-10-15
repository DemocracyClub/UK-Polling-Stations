from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E09000028"
    addresses_name = (
        "2020-02-17T14:30:02.399947/EC & Democracy Club Polling Place Look Up 2020.csv"
    )
    stations_name = (
        "2020-02-17T14:30:02.399947/EC & Democracy Club Polling Place Look Up 2020.csv"
    )
    elections = ["2020-05-07"]
    csv_delimiter = ","
