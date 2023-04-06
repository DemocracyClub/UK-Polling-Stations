from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "OAD"
    addresses_name = "2023-05-04/2023-04-04T17:54:00.271699/Democracy_Club__04May2023 (Rev. 04-04-2023).tsv"
    stations_name = "2023-05-04/2023-04-04T17:54:00.271699/Democracy_Club__04May2023 (Rev. 04-04-2023).tsv"
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10010146840",  # 46A LONG STREET, WIGSTON
        ]:
            return None

        if record.addressline6 in [
            # look wrong
            "LE18 2GQ",
            "LE18 3AN",
        ]:
            return None

        return super().address_record_to_dict(record)
