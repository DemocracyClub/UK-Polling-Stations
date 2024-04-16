from data_importers.management.commands import BaseHalaroseCsvImporter

COED_Y_GARN_PRIMARY_SCHOOL = {
    "pollingstationname": "COED-Y-GARN PRIMARY SCHOOL (NURSERY)",
    "pollingstationaddress_1": "PARROT ROW",
    "pollingstationaddress_2": "",
    "pollingstationaddress_3": "BLAINA",
    "pollingstationaddress_4": "",
    "pollingstationaddress_5": "",
    "pollingstationpostcode": "NP13 3AH",
    "pollingvenueuprn": "",
}


class Command(BaseHalaroseCsvImporter):
    council_id = "BGW"
    addresses_name = "2024-05-02/2024-03-20T09:59:04.174956/Eros_SQL_Output008.csv"
    stations_name = "2024-05-02/2024-03-20T09:59:04.174956/Eros_SQL_Output008.csv"
    elections = ["2024-05-02"]
    csv_encoding = "windows-1252"

    def station_record_to_dict(self, record):
        # station change from council:
        # old: COEDCAE COMMUNITY CENTRE, ATTLEE ROAD, NANTYGLO, NP23 4WB
        # new: COED-Y-GARN PRIMARY SCHOOL (NURSERY), PARROT ROW, BLAINA, NP13 3AH
        if self.get_station_hash(record) == "27-coedcae-community-centre":
            record = record._replace(**COED_Y_GARN_PRIMARY_SCHOOL)

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "100100460975",  # 27A QUEEN STREET, NANTYGLO
            "100100460974",  # 27B QUEEN STREET, NANTYGLO
            "10014116610",  # 1 MOUNTAIN AIR, EBBW VALE
            "10014116959",  # 8 RESERVOIR ROAD, BEAUFORT, EBBW VALE
        ]:
            return None

        if record.housepostcode in [
            "NP23 5DH",  # split
        ]:
            return None

        if self.get_station_hash(record) == "27-coedcae-community-centre":
            record = record._replace(**COED_Y_GARN_PRIMARY_SCHOOL)

        return super().address_record_to_dict(record)
