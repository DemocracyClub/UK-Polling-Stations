from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "DAL"
    addresses_name = (
        "2024-07-04/2024-06-04T12:41:40.204472/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-04T12:41:40.204472/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10003079870",  # LIMEKILN COTTAGE, PIERCEBRIDGE, DARLINGTON
            "100110539592",  # 51 COBDEN STREET, DARLINGTON
        ]:
            return None

        if record.addressline6 in [
            # split
            "DL1 2RG",
            # suspect
            "DL2 2UG",
        ]:
            return None

        return super().address_record_to_dict(record)
