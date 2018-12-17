from data_collection.management.commands import (
    BaseXpressDCCsvInconsistentPostcodesImporter,
)


class Command(BaseXpressDCCsvInconsistentPostcodesImporter):
    council_id = "E08000037"
    addresses_name = "parl.2017-06-08/Version 1/Democracy_Club__08June2017 (6).tsv"
    stations_name = "parl.2017-06-08/Version 1/Democracy_Club__08June2017 (6).tsv"
    elections = ["parl.2017-06-08"]
    csv_delimiter = "\t"
