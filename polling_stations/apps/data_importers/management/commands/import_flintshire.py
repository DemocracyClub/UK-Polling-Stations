from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "FLN"
    addresses_name = (
        "2022-05-05/2022-04-11T10:40:42.647159/Democracy_Club__05May2022 - FCC.CSV"
    )
    stations_name = (
        "2022-05-05/2022-04-11T10:40:42.647159/Democracy_Club__05May2022 - FCC.CSV"
    )
    elections = ["2022-05-05"]
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "CH7 3PF",
            "LL12 9HN",
            "CH5 3EF",
            "CH7 6PA",
            "CH7 6SD",
            "CH5 1PD",
            "LL12 9DU",
            "CH6 5TP",
            "CH7 3DG",
            "CH4 0PE",
            "CH7 2JR",
            "CH5 3LF",
            "CH7 6EH",
            "CH5 1QR",
            "CH7 6YX",
            "CH7 2HW",
            "CH7 6BA",
            "CH8 8JY",
            "CH7 6AH",
            "CH8 9NY",
            "CH7 2JP",
            "CH8 7ED",
            "CH8 7PQ",
            "CH7 6TH",
        ]:
            return None  # split

        return super().address_record_to_dict(record)
