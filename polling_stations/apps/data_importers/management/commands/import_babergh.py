from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BAB"
    addresses_name = "2026-05-07/2026-03-23T14:36:37.270467/BDC Democracy Club - Polling Districts.csv"
    stations_name = (
        "2026-05-07/2026-03-23T14:36:37.270467/BDC Democracy Club Polling Stations.csv"
    )
    elections = ["2026-05-07"]
    csv_encoding = "utf-8-sig"

    def address_record_to_dict(self, record):
        if record.uprn in [
            "10094142683",  # 3 SHUTTLE CLOSE, SUDBURY, CO10 1AS
            "10094142549",  # 33 FAWCETT ROAD, CHILTON, SUDBURY, CO10 0WX
            "10096562529",  # 31 LATHAM ROAD, HADLEIGH, IPSWICH, IP7 6SL
            "10096562502",  # 11 LATHAM ROAD, HADLEIGH, IPSWICH, IP7 6SL
            "10094142009",  # GREYCOTE RODBRIDGE HILL, LONG MELFORD
            "10093344109",  # 25 WAKELIN CLOSE, GREAT CORNARD, SUDBURY
            "100091457209",  # KINGSBURY HOUSE, UPPER ROAD, LITTLE CORNARD, SUDBURY
            "10094140064",  # ELM VIEW, STONE STREET, HADLEIGH, IPSWICH
            "10093344041",  # 10 GRACE FARRANT ROAD, GREAT CORNARD, SUDBURY
        ]:
            return None

        if record.postcode in [
            # split
            "CO10 9LN",
            "CO10 0PW",
            # suspect
            "CO10 2PQ",
            "IP7 6AB",
        ]:
            return None

        return super().address_record_to_dict(record)
