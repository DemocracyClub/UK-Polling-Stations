from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "DUD"
    addresses_name = (
        "2021-04-20T10:07:18.089598/Dudley Copy of Democracy_Club__06May2021.csv"
    )
    stations_name = (
        "2021-04-20T10:07:18.089598/Dudley Copy of Democracy_Club__06May2021.csv"
    )
    elections = ["2021-05-06"]
    csv_delimiter = ","
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "90157092",  # 74 HAYES LANE, STOURBRIDGE
            "90159047",  # THE JAYS, HYPERION ROAD, STOURTON, STOURBRIDGE
            "90153608",  # NEW BROMLEY FARM, BROMLEY LANE, KINGSWINFORD
            "90127392",  # FLAT A 106 STOURBRIDGE ROAD, DUDLEY
            "90135708",  # 106B STOURBRIDGE ROAD, DUDLEY
            "90142681",  # 106C STOURBRIDGE ROAD, DUDLEY
            "90163097",  # 50 WOLVERHAMPTON STREET, DUDLEY
            "90163098",  # 51 WOLVERHAMPTON STREET, DUDLEY
            "90163100",  # 52 WOLVERHAMPTON STREET, DUDLEY
            "90150770",  # HICKMERELANDS FARM, HICKMERELANDS, DUDLEY
            "90161895",  # FIRST FLOOR FLAT 166-167 WOLVERHAMPTON STREET, DUDLEY
        ]:
            return None

        if record.addressline6 in ["DY1 3EP", "DY5 2PA"]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):

        # Caravan on Land Adjoining Black Horse Illey Lane Illey Halesowen B62 0JH
        if record.polling_place_id == "24813":
            record = record._replace(polling_place_postcode="B62 0HJ")

        # Rufford Primary School Bredon Avenue Stourbridge DY9 7RN
        if record.polling_place_id == "24895":
            record = record._replace(polling_place_postcode="DY9 7NR")

        return super().station_record_to_dict(record)
