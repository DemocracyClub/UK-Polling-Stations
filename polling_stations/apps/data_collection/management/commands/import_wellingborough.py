from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000156"
    addresses_name = (
        "europarl.2019-05-23/Version 1/DC Polling Station Data Wellingborough.CSV"
    )
    stations_name = (
        "europarl.2019-05-23/Version 1/DC Polling Station Data Wellingborough.CSV"
    )
    elections = ["europarl.2019-05-23"]
