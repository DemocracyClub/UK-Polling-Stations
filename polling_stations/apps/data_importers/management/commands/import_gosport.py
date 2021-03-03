from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "GOS"
    addresses_name = "2021-03-02T17:11:51.716352/2021 LGE & PCC - Gosport Democracy_Club__06May2021 v2.tsv"
    stations_name = "2021-03-02T17:11:51.716352/2021 LGE & PCC - Gosport Democracy_Club__06May2021 v2.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in ["PO13 0EW"]:
            return None

        return super().address_record_to_dict(record)
