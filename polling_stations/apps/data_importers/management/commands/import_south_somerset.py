from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "SSO"
    addresses_name = "2024-07-04/2024-06-21T16:02:50.306102/SSO_combined.csv"
    stations_name = "2024-07-04/2024-06-21T16:02:50.306102/SSO_combined.csv"
    elections = ["2024-07-04"]
    not_in_sso_stations = [
        "1-glastonbury-town-hall",
        "10-street-salvation-army-hall",
        "11-baltonsborough-village-hall",
        "12-butleigh-church-room",
        "13-west-lydford-parish-hall",
        "2-glastonbury-st-edmunds-community-hall",
        "3-glastonbury-united-reformed-church",
        "4-glastonbury-town-hall",
        "5-street-salvation-army-hall",
        "6-street-united-reformed-church",
        "7-street-wessex-hotel",
        "8-street-the-victoria-field-social-club",
        "9-street-the-victoria-field-social-club",
    ]

    def station_record_to_dict(self, record):
        station_hash = self.get_station_hash(record)
        if station_hash in self.not_in_sso_stations:
            return None
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        station_hash = self.get_station_hash(record)
        if station_hash in self.not_in_sso_stations:
            return None
        if record.housepostcode in [
            # split
            "TA20 2NJ",
            "BA10 0BU",
            "BA9 9NZ",
            "TA20 2BE",
            "TA10 0HF",
            "BA22 8NT",
            "TA3 6RP",
            "TA10 0PJ",
            "TA10 0QH",
            "TA18 8BT",
        ]:
            return None
        return super().address_record_to_dict(record)
