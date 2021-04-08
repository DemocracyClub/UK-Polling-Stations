from data_importers.ems_importers import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SNR"
    addresses_name = "2021-04-08T13:23:29.076733/Democracy_Club__06May2021.tsv"
    stations_name = "2021-04-08T13:23:29.076733/Democracy_Club__06May2021.tsv"
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"  # "Narrowboat L’eau Life"
    elections = ["2021-05-06"]

    # - As % of rows in council csv   : 33.3%
    # because there are three rows for every property (one per election type)

    # This has been checked, and is okay:
    # WARNING: Polling stations 'Sure Start Children`s Centre The Community Centre' and
    # 'A5 Rangers Clubroom 101 Watling Street' are at approximately the same location

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "NN7 3NS",  # spurious distance
        ]:
            return None

        return super().address_record_to_dict(record)
