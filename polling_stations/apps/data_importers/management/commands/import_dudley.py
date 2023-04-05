from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "DUD"
    addresses_name = (
        "2023-05-04/2023-03-26T19:37:35.489411/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-26T19:37:35.489411/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "90159047",  # THE JAYS, HYPERION ROAD, STOURTON, STOURBRIDGE
            "90153608",  # NEW BROMLEY FARM, BROMLEY LANE, KINGSWINFORD
            "90135708",  # 106B STOURBRIDGE ROAD, DUDLEY
            "90142681",  # 106C STOURBRIDGE ROAD, DUDLEY
            "90163097",  # 50 WOLVERHAMPTON STREET, DUDLEY
            "90163098",  # 51 WOLVERHAMPTON STREET, DUDLEY
            "90163100",  # 52 WOLVERHAMPTON STREET, DUDLEY
            "90147692",  # SCHOOL HOUSE, COTWALL END ROAD, DUDLEY
            "90056006",  # 1 BELLS LANE, STOURBRIDGE
            "90151695",  # HURST LEA, PEDMORE ROAD, BRIERLEY HILL
            "90202527",  # LIVING ACCOMMODATION HINDU CULTURAL CENTRE 57-59 KING STREET, DUDLEY
        ]:
            return None

        if record.addressline6 in [
            # split
            "DY1 3EP",
            "DY6 7LT",
            "DY8 4LU",  # ADJACENT THE BONDED WAREHOUSE CANAL STREET, AMBLECOTE
            "DY2 8QB",  # THE OLD VICARAGE, KING STREET, DUDLEY
        ]:
            return None

        return super().address_record_to_dict(record)
