from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RUG"
    addresses_name = (
        "2026-05-07/2026-03-16T17:37:18.372246/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-16T17:37:18.372246/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "10010514865",  # BIRCH COTTAGE, SCHOOL STREET, LONG LAWFORD, RUGBY, CV23 9AT
                "10010514866",  # CHERRY TREE COTTAGE, SCHOOL STREET, LONG LAWFORD, RUGBY, CV23 9AT
                "10094756087",  # 246 NEWBOLD ROAD, RUGBY
                "100071238030",  # 2 CONSUL ROAD, RUGBY
                "10010512059",  # 149 HILLMORTON ROAD, RUGBY
                "100070176487",  # 232 ALWYN ROAD, BILTON, RUGBY
                "100071239364",  # PENINSULAR FARM, MAIN STREET, NEWBOLD, RUGBY
                "10010518581",  # FOXLEY BARN, SOUTHAM ROAD, KITES HARDWICK, RUGBY
            ]
        ):
            return None

        if record.addressline6 in [
            # suspect
            "CV22 7YF",
            "CV22 7ND",
        ]:
            return None

        return super().address_record_to_dict(record)
