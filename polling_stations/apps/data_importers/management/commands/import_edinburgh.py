from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "EDH"
    addresses_name = "2024-07-04/2024-06-05T12:18:26.898141/Eros_SQL_Output002.csv"
    stations_name = "2024-07-04/2024-06-05T12:18:26.898141/Eros_SQL_Output002.csv"
    elections = ["2024-07-04"]
    csv_encoding = "windows-1252"

    def station_record_to_dict(self, record):
        # Removing the following stations that are outside of the council area and have no addresses assigned
        if self.get_station_hash(record) in [
            "7-north-esk-parish-church-hall",  # North Esk Parish Church Hall, 16 Bridge Street, Musselburgh
            "5-north-esk-parish-church-hall",  # North Esk Parish Church Hall, 16 Bridge Street, Musselburgh
            "6-north-esk-parish-church-hall",  # North Esk Parish Church Hall, 16 Bridge Street, Musselburgh
            "1-musselburgh-rugby-football-club",  # Musselburgh Rugby Football Club, 3A Stoneyhill Farm Road, Musselburgh
            "2-musselburgh-rugby-football-club",  # Musselburgh Rugby Football Club, 3A Stoneyhill Farm Road, Musselburgh
            "3-musselburgh-rugby-football-club",  # Musselburgh Rugby Football Club, 3A Stoneyhill Farm Road, Musselburgh
            "4-musselburgh-rugby-football-club",  # Musselburgh Rugby Football Club, 3A Stoneyhill Farm Road, Musselburgh
            "8-our-lady-of-loretto-church-hall",  # Our Lady Of Loretto Church Hall, 17 Newbigging, Musselburgh
            "9-our-lady-of-loretto-church-hall",  # Our Lady Of Loretto Church Hall, 17 Newbigging, Musselburgh
        ]:
            return None
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "906499809",  # 365A BROOMHOUSE ROAD, EDINBURGH
        ]:
            return None

        if record.housepostcode in [
            # splits
            "EH16 6XE",
            "EH7 4QJ",
            "EH16 4TW",
            "EH16 5TQ",
            "EH11 1JU",
            "EH14 7AB",
            "EH11 4NU",
            "EH10 5RF",
            "EH11 1DU",
            "EH6 7FL",
            "EH6 7FN",
            "EH29 9FQ",
            "EH6 8DQ",
            "EH7 6LG",
            "EH13 0DA",
            "EH5 2DJ",
            "EH29 9FS",
            "EH7 6AW",
            "EH5 2DN",
            "EH4 7AW",
        ]:
            return None
        return super().address_record_to_dict(record)
