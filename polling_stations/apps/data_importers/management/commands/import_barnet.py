from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BNE"
    addresses_name = "2025-03-06/2025-02-10T12:43:03.278468/districts-merged.csv"
    stations_name = "2025-03-06/2025-02-10T12:43:03.278468/stations-merged.csv"
    elections = ["2025-02-13"]
    """
    Note: Normally files from Democracy Counts are UTF16-LE
    In this case, the council sent us
    - some files that they had exported from Democracy Counts
    - a file they had manually edited in a spreadsheet
    and I had to merge them together.
    The path of least resistance here was to covert everything to UTF-8
    so the files we're importing here are UTF-8 but next time we do an
    importer for this council they will probably be UTF16-LE again
    """
    csv_encoding = "utf-8"
