from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RUG"
    addresses_name = (
        "2025-05-01/2025-03-14T16:20:08.427955/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-14T16:20:08.427955/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10094756087",  # 246 NEWBOLD ROAD, RUGBY
            "100071238030",  # 2 CONSUL ROAD, RUGBY
            "10010512059",  # 149 HILLMORTON ROAD, RUGBY
            "100070176487",  # 232 ALWYN ROAD, BILTON, RUGBY
            "100071239364",  # PENINSULAR FARM, MAIN STREET, NEWBOLD, RUGBY
            "10010518581",  # FOXLEY BARN, SOUTHAM ROAD, KITES HARDWICK, RUGBY
        ]:
            return None

        if record.addressline6 in [
            # suspect
            "CV22 7YF",
            "CV22 7ZX",
        ]:
            return None

        return super().address_record_to_dict(record)
