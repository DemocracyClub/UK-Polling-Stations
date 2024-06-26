from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RUG"
    addresses_name = "2024-07-04/2024-06-26T11:33:52.388735/RUG_combined.tsv"
    stations_name = "2024-07-04/2024-06-26T11:33:52.388735/RUG_combined.tsv"
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # suspect
            "CV22 7YF",
            "CV22 7ZX",
        ]:
            return None
        return super().address_record_to_dict(record)
