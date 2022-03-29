from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "DEN"
    addresses_name = (
        "2022-05-05/2022-03-23T09:46:47.855229/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-23T09:46:47.855229/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    # 200004299740 (YR HEN FELIN, LLANNEFYDD ROAD, HENLLAN, DENBIGH) looks
    # fine, as it's on the other side of an administrative boundary.
