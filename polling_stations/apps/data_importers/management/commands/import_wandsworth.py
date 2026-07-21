from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WND"
    addresses_name = (
        "2026-08-27/2026-07-21T10:49:48.380732/Democracy_Club__27August2026.tsv"
    )
    stations_name = (
        "2026-08-27/2026-07-21T10:49:48.380732/Democracy_Club__27August2026.tsv"
    )
    elections = ["2026-08-27"]
    csv_delimiter = "\t"

    # maintaining tweaks through by-election
    # def address_record_to_dict(self, record):
    #     uprn = record.property_urn.strip().lstrip("0")

    #     if uprn in [
    #         "100022701958",  # 5 THURLEIGH MANSIONS 33 THURLEIGH ROAD, LONDON
    #         "100023328601",  # THE COTTAGE, MAGDALEN ROAD, LONDON
    #     ]:
    #         return None

    #     if record.addressline6 in [
    #         # split
    #         "SW12 9RF",
    #     ]:
    #         return None

    #     return super().address_record_to_dict(record)
