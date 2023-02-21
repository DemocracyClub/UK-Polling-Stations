from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MOL"
    addresses_name = (
        "2022-05-05/2022-03-18T10:50:42.011286/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-18T10:50:42.011286/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10010534294",
            "10010537566",
            "10010536978",
            "10010536968",
        ]:
            return None

        if record.addressline6 in ["KT21 2HL", "KT22 9QD"]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        return super().station_record_to_dict(record)
