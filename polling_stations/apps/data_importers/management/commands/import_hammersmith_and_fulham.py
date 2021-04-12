from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "HMF"
    addresses_name = "2021-04-12T09:04:13.301934/polling_station_export-2021-04-11.csv"
    stations_name = "2021-04-12T09:04:13.301934/polling_station_export-2021-04-11.csv"
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "34150747",  # FLAT 1, 62A RYLETT ROAD, LONDON
            "34150748",  # FLAT 2, 62A RYLETT ROAD, LONDON
            "34152305",  # 2A NITON STREET, LONDON
            "34155328",  # 29C MUNSTER ROAD, LONDON
            "34136009",  # UPPER FLOOR INNER LODGE ST MARY'S CEMETERY HARROW ROAD, WEMBLEY
            "34135797",  # GROUND FLOOR INNER LODGE ST MARY'S CEMETERY HARROW ROAD, WEMBLEY
            "34146774",  # THIRD FLOOR FLAT 95 HAMMERSMITH GROVE, LONDON
        ]:
            return None

        if record.housepostcode in [
            "W14 9DS",
            "W6 9HJ",
            "SW6 2EF",
            "SW6 2GG",
            "SW6 2GN",
            "W14 8UZ",
        ]:
            return None

        return super().address_record_to_dict(record)
