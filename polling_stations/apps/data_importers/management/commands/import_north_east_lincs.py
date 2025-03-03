from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "NEL"
    addresses_name = "2025-05-01/2025-03-03T14:56:37.387375/Eros_SQL_Output004.csv"
    stations_name = "2025-05-01/2025-03-03T14:56:37.387375/Eros_SQL_Output004.csv"
    elections = ["2025-05-01"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if (
            uprn
            in [
                "10090078903",  # FLAT, 247 GRIMSBY ROAD, CLEETHORPES
                "10090086605",  # THE ROOST, DIANA PRINCESS OF WALES HOSPITAL, SCARTHO ROAD, GRIMSBY
                "10090078890",  # FLAT 3, 50 RUTLAND STREET, GRIMSBY
                "10090078888",  # FLAT 1, 50 RUTLAND STREET, GRIMSBY
                "10090078889",  # FLAT 2, 50 RUTLAND STREET, GRIMSBY
                "10090078891",  # FLAT 4, 50 RUTLAND STREET, GRIMSBY
                "11023550",  # 38 BRAMHALL STREET, CLEETHORPES
                "11088787",  # 4 WALTHAM HOUSE FARM COTTAGE, LOUTH ROAD, NEW WALTHAM, GRIMSBY
                "11088786",  # WALTHAM HOUSE FARM COTTAGE 3 LOUTH ROAD, WALTHAM
            ]
        ):
            return None

        if record.housepostcode in [
            # split
            "DN35 0RA",
            # suspect
            "DN37 0BN",
        ]:
            return None
        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        if record.pollingvenueid == "19":
            # point for this one is in the North Sea
            # delete the grid ref and use UPRN instead
            record = record._replace(pollingvenueeasting="0")
            record = record._replace(pollingvenuenorthing="0")
        return super().station_record_to_dict(record)
