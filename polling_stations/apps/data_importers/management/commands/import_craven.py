from data_importers.management.commands import (
    BaseXpressDCCsvInconsistentPostcodesImporter,
)


class Command(BaseXpressDCCsvInconsistentPostcodesImporter):
    council_id = "CRA"
    addresses_name = "2021-11-17T10:33:36.800611/Democracy_Club__25November2021.tsv"
    stations_name = "2021-11-17T10:33:36.800611/Democracy_Club__25November2021.tsv"
    elections = ["2021-11-25"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"
