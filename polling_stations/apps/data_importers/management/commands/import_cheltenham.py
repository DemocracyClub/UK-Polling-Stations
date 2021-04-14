from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "CHT"
    addresses_name = (
        "2021-03-25T14:01:18.317528/Cheltenham polling_station_export-2021-03-24.csv"
    )
    stations_name = (
        "2021-03-25T14:01:18.317528/Cheltenham polling_station_export-2021-03-24.csv"
    )
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "200002686059",  # 3A CLARENCE ROAD, CHELTENHAM
            "100120409897",  # BUXTON, NAUNTON LANE, CHELTENHAM
            "200001494338",  # BASEMENT FLAT, NORTHWICK, DOURO ROAD, CHELTENHAM
            "10091671112",  # FLAT ABOVE, SOUND & VISION EXPRESS LTD, MEAD ROAD, CHELTENHAM
        ]:
            return None

        if record.housepostcode in [
            "GL52 2ES",
            "GL53 7AJ",
            "GL52 6RN",
            "GL53 0HL",
            "GL50 2DZ",
            "GL50 3RB",
        ]:
            return None

        return super().address_record_to_dict(record)
