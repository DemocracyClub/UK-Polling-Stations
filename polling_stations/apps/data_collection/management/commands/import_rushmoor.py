from data_collection.management.commands import (
    BaseXpressDCCsvInconsistentPostcodesImporter,
)


class Command(BaseXpressDCCsvInconsistentPostcodesImporter):
    council_id = "E07000092"
    addresses_name = "local.2018-05-03/Version 1/Democracy_Club__03May2018.tsv"
    stations_name = "local.2018-05-03/Version 1/Democracy_Club__03May2018.tsv"
    elections = ["local.2018-05-03"]
    csv_delimiter = "\t"
