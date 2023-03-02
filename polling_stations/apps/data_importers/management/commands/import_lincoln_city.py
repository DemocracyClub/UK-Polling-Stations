from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "LIC"
    addresses_name = "2023-05-04/2023-03-08T08:30:56.391353/Eros_SQL_Output003.csv"
    stations_name = "2023-05-04/2023-03-08T08:30:56.391353/Eros_SQL_Output003.csv"
    elections = ["2023-05-04"]

    def station_record_to_dict(self, record):
        # Have checked THE LINCOLN GREEN PUBLIC HOUSE - THE BAR STATION (out of area), and it's fine

        # CHURCH OF JESUS CHRIST OF LATTER DAY SAINTS STATION 47, SKELLINGTHORPE ROAD, LINCOLN
        # has a different postcode attested on the web (LN6 0QJ), but AddressBase has the
        # council-provided one (LN6 0PB) as being for exactly the one building that is the church,
        # so we'll leave it be.

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            "LN1 3SL",
            # split
            "LN1 1DR",
            "LN1 1XE",
            "LN1 3BS",
            "LN2 4DY",
            "LN2 4NA",
            "LN2 4PA",
            "LN2 5EJ",
            "LN2 5HZ",
            "LN5 7LA",
            "LN5 8AG",
            "LN6 0HX",
            "LN6 0LH",
            "LN6 8AZ",
            "LN6 8DB",
        ]:
            return None

        return super().address_record_to_dict(record)
