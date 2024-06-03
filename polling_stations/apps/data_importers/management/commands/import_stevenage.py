from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "STV"
    addresses_name = "2024-07-04/2024-06-11T12:21:03.880800/Democracy Club - Polling Districts UTF-8.csv"
    stations_name = (
        "2024-07-04/2024-06-11T12:21:03.880800/Democracy Club - Polling Stations.csv"
    )
    elections = ["2024-07-04"]

    def station_record_to_dict(self, record):
        # The following stations are not in the council are and have no addresses associated:
        if record.stationcode in [
            "ADW1-46",  # ASTON VILLAGE HALL, 9 NEW PARK LANE, ASTON, HERTS
            "ADW2-47",  # DATCHWORTH VILLAGE HALL, THE GREEN, DATCHWORTH
            "S-KN-1-43",  # KNEBWORTH VILLAGE HALL, PARK LANE, KNEBWORTH
            "S-KN-2-44",  # KNEBWORTH VILLAGE HALL, PARK LANE, KNEBWORTH
            "S-KN-CDE-45",  # JOHN CLEMENTS SPORTS & COMMUNITY CENTRE, BURY LANE, CODICOTE, HITCHIN
            "S-CK-CVL-42",  # PEACE MEMORIAL HALL, HIGH STREET, CODICOTE, HITCHIN
        ]:
            return None
        return super().station_record_to_dict(record)
