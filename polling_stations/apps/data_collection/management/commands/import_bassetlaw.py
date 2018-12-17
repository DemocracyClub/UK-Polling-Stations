from data_collection.management.commands import (
    BaseXpressDCCsvInconsistentPostcodesImporter,
)


class Command(BaseXpressDCCsvInconsistentPostcodesImporter):
    council_id = "E07000171"
    addresses_name = (
        "parl.2017-06-08/Version 1/Bassetlaw Democracy_Club__08June2017.tsv"
    )
    stations_name = "parl.2017-06-08/Version 1/Bassetlaw Democracy_Club__08June2017.tsv"
    elections = ["parl.2017-06-08"]
    csv_delimiter = "\t"
