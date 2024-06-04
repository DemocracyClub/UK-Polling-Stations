from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "CHT"
    addresses_name = "2024-07-04/2024-06-04T14:53:31.031794/Eros_SQL_Output011.csv"
    stations_name = "2024-07-04/2024-06-04T14:53:31.031794/Eros_SQL_Output011.csv"
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "100121229562",  # THE MEWS, BACK MONTPELLIER TERRACE, CHELTENHAM
            "200002684616",  # 49A BACK MONTPELLIER TERRACE, CHELTENHAM
            "100120413433",  # FLAT, 19 SUFFOLK ROAD, CHELTENHAM
            "100120399951",  # FARROW & BALL, 15-17 SUFFOLK ROAD, CHELTENHAM
            "10091672800",  # HOLLY BLUE HOUSE, LONDON ROAD, CHELTENHAM
        ]:
            return None

        if record.housepostcode in [
            # split
            "GL50 3RB",
            "GL52 2ES",
            "GL52 6RN",
            "GL53 0HL",
            "GL50 2RF",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Below stations are throwing a warning about different postcode in the addressbase, but council requested to keep them.
        # HILLVIEW COMMUNITY CENTRE, HULBERT CRESCENT, UP HATHERLEY, CHELTENHAM, GL51 3EB
        # OAKLEY COMMUNITY, RESOURCE CENTRE, CLYDE CRESCENT, CHELTENHAM, GL52 5QL

        return super().station_record_to_dict(record)
