from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E06000004"
    addresses_name = "local.2019-05-02/Version 2/stockton.gov.uk-1554713389000.tsv"
    stations_name = "local.2019-05-02/Version 2/stockton.gov.uk-1554713389000.tsv"
    elections = ["local.2019-05-02"]
    csv_delimiter = "\t"
