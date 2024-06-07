from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "ABD"
    addresses_name = (
        "2024-07-04/2024-06-07T15:42:14.722645/Eros_SQL_Output002 - Aberdeenshire.csv"
    )
    stations_name = (
        "2024-07-04/2024-06-07T15:42:14.722645/Eros_SQL_Output002 - Aberdeenshire.csv"
    )
    elections = ["2024-07-04"]

    def station_record_to_dict(self, record):
        # Skip stations that are not in Aberdeenshire
        if self.get_station_hash(record) in [
            "68-function-hall",
            "69-function-hall",
            "70-buckie-methodist-church-hall",
            "72-royal-british-legion-hall",
            "71-north-church-hall",
            "73-royal-british-legion-hall",
            "74-portessie-methodist-church-hall",
            "60-cullen-bowling-and-tennis-club",
            "61-deskford-jubilee-hall",
            "59-mcboyle-hall",
            "75-town-hall",
            "76-spey-bay-hall",
            "78-fochabers-public-institute",
            "79-fochabers-public-institute",
            "80-clochan-community-hall",
            "65-longmore-halls",
            "66-longmore-halls",
            "64-old-ogilvie-school-hall",
            "63-king-memorial-hall-off-a95",
            "67-rothiemay-school",
            "62-newmill-public-hall",
        ]:
            return None

        # corrects wrong postcode for: TOWIE PUBLIC HALL, TOWIE, GLENKINDIE, ALFORD AB33 8NR
        if self.get_station_hash(record) in [
            "23-towie-public-hall",
            "24-towie-public-hall",
        ]:
            record = record._replace(pollingstationpostcode="AB33 8RN")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "151176868",  # THE BLACK HOUSE, NEWBURGH, ELLON
            "151176475",  # CARAVAN 5 DYKELANDS FARM A937 SOUTH BALMAKELLY ACCESS ROAD TO A90T SOUTH OF LAURENCEKIRK, LAURENCEKIRK
        ]:
            return None
        if record.housepostcode in [
            # splits
            "AB21 0QJ",
            "AB51 0UZ",
            "AB51 8XH",
            "AB41 7UA",
            "AB39 2UJ",
            "AB42 5JB",
            "AB35 5PR",
            "AB51 5DU",
            "AB43 7AR",
        ]:
            return None
        return super().address_record_to_dict(record)
