from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "CHT"
    addresses_name = "2025-05-01/2025-02-28T13:01:36.708211/Eros_SQL_Output007.csv"
    stations_name = "2025-05-01/2025-02-28T13:01:36.708211/Eros_SQL_Output007.csv"
    elections = ["2025-05-01"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "100121229562",  # THE MEWS, BACK MONTPELLIER TERRACE, CHELTENHAM
            "200002684616",  # 49A BACK MONTPELLIER TERRACE, CHELTENHAM
            "100120413433",  # FLAT, 19 SUFFOLK ROAD, CHELTENHAM
            "100120399951",  # FARROW & BALL, 15-17 SUFFOLK ROAD, CHELTENHAM
        ]:
            return None

        if record.housepostcode in [
            # split
            "GL52 6RN",
            "GL50 2RF",
            "GL52 2ES",
            "GL50 3RB",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Below stations are throwing a warning about different postcode in the addressbase, but council requested to keep them.
        # HILLVIEW COMMUNITY CENTRE, HULBERT CRESCENT, UP HATHERLEY, CHELTENHAM, GL51 3EB
        # OAKLEY COMMUNITY, RESOURCE CENTRE, CLYDE CRESCENT, CHELTENHAM, GL52 5QL

        return super().station_record_to_dict(record)
