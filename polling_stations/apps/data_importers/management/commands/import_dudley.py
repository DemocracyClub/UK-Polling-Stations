from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "DUD"
    addresses_name = (
        "2022-05-05/2022-04-13T09:59:32.342801/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-04-13T09:59:32.342801/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "90159047",  # THE JAYS, HYPERION ROAD, STOURTON, STOURBRIDGE
            "90153608",  # NEW BROMLEY FARM, BROMLEY LANE, KINGSWINFORD
            "90127392",  # FLAT A 106 STOURBRIDGE ROAD, DUDLEY
            "90135708",  # 106B STOURBRIDGE ROAD, DUDLEY
            "90142681",  # 106C STOURBRIDGE ROAD, DUDLEY
            "90163097",  # 50 WOLVERHAMPTON STREET, DUDLEY
            "90163098",  # 51 WOLVERHAMPTON STREET, DUDLEY
            "90163100",  # 52 WOLVERHAMPTON STREET, DUDLEY
        ]:
            return None

        if record.addressline6 in ["DY1 3EP"]:
            return None  # split

        return super().address_record_to_dict(record)
