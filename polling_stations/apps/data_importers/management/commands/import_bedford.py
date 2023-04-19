from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BDF"
    addresses_name = (
        "2023-05-04/2023-04-19T10:28:35.386737/Democracy Club - Polling Districts.csv"
    )
    stations_name = (
        "2023-05-04/2023-04-19T10:28:35.386737/Democracy Club - Polling Stations.csv"
    )
    elections = ["2023-05-04"]

    def station_record_to_dict(self, record):
        # Lots of dodgy looking points
        if record.stationcode.strip() in [
            "76",  # WOOTTON MEMORIAL HALL
            "81",  # WOOTTON MEMORIAL HALL
            "78",  # Wootton Community Centre
            "79",  # Wootton Community Centre
            "80",  # Wootton Community Centre
            "39",  # CRYSELCO PAVILION
            "31",  # PARK ROAD METHODIST CHURCH
            "32",  # PARK ROAD METHODIST CHURCH
            "42",  # SPRINGFIELD SCHOOL
            "43",  # SPRINGFIELD SCHOOL
            "10",  # BEDFORD HOSPITAL
        ]:
            record = record._replace(xordinate="", yordinate="")

        return super().station_record_to_dict(record)
