from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "NEL"
    addresses_name = "2024-05-02/2024-03-12T11:47:38.056186/Eros_SQL_Output004.csv"
    stations_name = "2024-05-02/2024-03-12T11:47:38.056186/Eros_SQL_Output004.csv"
    elections = ["2024-05-02"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10090078903",  # FLAT, 247 GRIMSBY ROAD, CLEETHORPES
            "10090086605",  # THE ROOST, DIANA PRINCESS OF WALES HOSPITAL, SCARTHO ROAD, GRIMSBY
            "10090078890",  # FLAT 3, 50 RUTLAND STREET, GRIMSBY
            "10090078888",  # FLAT 1, 50 RUTLAND STREET, GRIMSBY
            "10090078889",  # FLAT 2, 50 RUTLAND STREET, GRIMSBY
            "10090078891",  # FLAT 4, 50 RUTLAND STREET, GRIMSBY
            "11023550",  # 38 BRAMHALL STREET, CLEETHORPES
            "11088787",  # 4 WALTHAM HOUSE FARM COTTAGE, LOUTH ROAD, NEW WALTHAM, GRIMSBY
            "11088786",  # WALTHAM HOUSE FARM COTTAGE 3 LOUTH ROAD, WALTHAM
        ]:
            return None

        return super().address_record_to_dict(record)
