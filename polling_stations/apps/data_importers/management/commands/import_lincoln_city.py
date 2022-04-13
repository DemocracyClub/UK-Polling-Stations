from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "LIC"
    addresses_name = (
        "2022-05-05/2022-04-13T14:01:42.242396/polling_station_export-2022-04-13.csv"
    )
    stations_name = (
        "2022-05-05/2022-04-13T14:01:42.242396/polling_station_export-2022-04-13.csv"
    )
    elections = ["2022-05-05"]

    def station_record_to_dict(self, record):
        # Have checked THE LINCOLN GREEN PUBLIC HOUSE - THE BAR STATION (out of area), and it's fine

        # CHURCH OF JESUS CHRIST OF LATTER DAY SAINTS STATION 47, SKELLINGTHORPE ROAD, LINCOLN
        # has a different postcode attested on the web (LN6 0QJ), but AddressBase has the
        # council-provided one (LN6 0PB) as being for exactly the one building that is the church,
        # so we'll leave it be.
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            "LN5 7LA",
            "LN2 4NA",
            "LN5 8AG",
            "LN6 0HX",
            "LN1 1AW",
            "LN5 8RT",
            "LN2 5LY",
            "LN6 0LU",
            "LN1 3BS",
            "LN2 5EJ",
            "LN2 5HZ",
            "LN6 8DB",
            "LN2 4DY",
            "LN6 8AZ",
            "LN2 4PA",
            "LN6 0LH",
            "LN1 1DR",
            "LN1 1XE",
        ]:
            return None  # split

        return super().address_record_to_dict(record)
