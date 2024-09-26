from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "MEN"
    addresses_name = "2024-07-04/2024-06-21T15:57:24.816333/MEN_combined.csv"
    stations_name = "2024-07-04/2024-06-21T15:57:24.816333/MEN_combined.csv"
    elections = ["2024-07-04"]
    not_in_mendip_stations = [
        "80-ilchester-town-hall-no2",
        "79-ilchester-town-hall-no1",
        "78-marston-magna-village-hall",
        "77-rimpton-village-hall",
        "76-corton-denham-village-hall",
        "75-wincanton-memorial-hall",
        "74-wincanton-memorial-hall",
        "73-the-davis-hall",
        "72-united-reformed-church-hall",
        "71-tintinhull-village-hall",
        "70-bayford-village-hall",
        "69-sparkford-village-hall",
        "68-sutton-montis-village-hall",
        "67-stoke-sub-hamdon-memorial-hall",
        "66-wessex-rooms",
        "65-wessex-rooms",
        "64-queen-camel-memorial-hall",
        "63-pitney-village-hall",
        "62-hadspen-village-hall",
        "61-pen-selwood-village-hall",
        "60-north-cheriton-village-hall",
        "59-norton-sub-hamdon-village-hall",
        "58-north-cadbury-village-hall",
        "57-mudford-village-hall",
        "56-muchelney-abbey",
        "554-wedmore-village-hall",
        "553-theale-village-hall",
        "552-blackford-village-hall",
        "551-weare-memorial-hall",
        "550-shipham-village-hall",
        "55-montacute-village-hall",
        "549-mark-village-hall",
        "548-lympsham-sports-club",
        "547-east-brent-village-hall",
        "546-cross-memorial-hall",
        "545-cheddar-village-hall-formerly-the-church-house",
        "544-cheddar-village-hall-formerly-the-church-house",
        "543-cheddar-village-hall-formerly-the-church-house",
        "542-the-old-schoolroom",
        "541-brent-knoll-parish-hall",
        "540-biddisham-parish-hall",
        "54-the-camelot-room-milborne-port-village-hall",
        "539-axbridge-town-hall",
        "538-stawell-village-hall",
        "537-shapwick-village-hall",
        "536-moorlinch-church-hall",
        "535-edington-village-hall",
        "534-east-huntspill-village-hall",
        "533-chilton-polden-village-hall",
        "532-edington-village-hall",
        "531-burtle-village-hall",
        "530-ashcott-village-hall",
        "53-the-camelot-room-milborne-port-village-hall",
        "52-martock-youth-centre-nos12",
        "51-martock-youth-centre-nos12",
        "50-north-barrow-village-hall",
        "49-long-load-village-hall",
        "48-long-sutton-village-hall",
        "47-ridgeway-hall",
        "46-kingsdon-village-hall",
        "45-the-church-rooms",
        "44-keinton-mandeville-village-hall",
        "43-barton-st-david-village-hall",
        "42-all-saints-church",
        "41-isle-abbotts-village-hall",
        "40-merryfield-hall",
        "39-huish-leisure-lifestyle-fitness-langport",
        "38-st-margarets-hall",
        "37-high-ham-village-hall",
        "36-henstridge-village-hall",
        "35-hambridge-village-hall",
        "34-fivehead-village-hall",
        "33-drayton-village-hall",
        "32-curry-rivel-village-hall",
        "31-curry-rivel-village-hall",
        "30-curry-mallet-and-beercrocombe-village-hall",
        "29-cucklington-village-hall",
        "28-chilthorne-domer-village-hall",
        "27-blackford-reading-room",
        "26-compton-dundon-village-hall",
        "25-charlton-musgrove-memorial-hall",
        "24-charlton-mackrell-reading-room",
        "23-charlton-horethorne-village-hall",
        "22-the-market-house",
        "21-caryford-hall",
        "20-bruton-community-hall",
        "19-brewham-village-hall",
        "18-martock-united-reformed-church-hall",
        "17-barrington-village-hall",
        "16-babcary-playing-field-hut",
        "15-ash-village-hall",
        "14-aller-village-hall",
    ]

    def address_record_to_dict(self, record):
        station_hash = self.get_station_hash(record)
        if station_hash in self.not_in_mendip_stations:
            return None
        uprn = record.uprn.strip().lstrip("0")

        if (
            uprn
            in [
                "250056648",  # WILLS FARM, PRIDDY, WELLS
                "250045108",  # ORCHARD BYRE, POLSHAM, WELLS
                "250070118",  # NEW MANOR FARM, POLSHAM, WELLS
                "250003895",  # TWIN OAKS, SOMERTON ROAD, STREET
                "250003837",  # LEIGHOLT FARM, SOMERTON ROAD, STREET
                "250081238",  # FLAT 1, 13 PRINTWORKS ROAD, FROME
                "250081239",  # FLAT 2, 13 PRINTWORKS ROAD, FROME
                "250070558",  # THE BELL TOWER ORCHARDLEIGH VILLAGE PUMP TO LULLINGTON LANE, LULLINGTON, FROME
                "250070559",  # THE CLOCK TOWER ORCHARDLEIGH VILLAGE PUMP TO LULLINGTON LANE, LULLINGTON, FROME
                "250046922",  # HEARTY GATE BUNGALOW, NORTH WOOTTON, SHEPTON MALLET
            ]
        ):
            return None

        if record.housepostcode in [
            # split
            "BA16 0NU",
            "BA4 4DP",
            "BA11 2ED",
            "BA11 5BT",
            "BA11 4SA",
            "BA11 2TQ",
            "BA11 2XG",
            "BA11 1NB",
            "BA16 0BD",
            "BA11 4AJ",
            "BA5 1RJ",
            "BA11 5HA",
            "BA6 9DH",
            "BA11 2AU",
            "BA11 5DU",
            "BA4 6SY",
            "BA3 5QE",
            "BA3 4DN",
            "BA11 5EP",
            "BA11 4NY",
            "BA4 5HB",
            # suspect
            "BA11 5FE",  # MARIGOLD ROAD
            "BA11 1GN",  # PRINTWORKS ROAD
        ]:
            return None
        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        station_hash = self.get_station_hash(record)
        if station_hash in self.not_in_mendip_stations:
            return None

        return super().station_record_to_dict(record)
