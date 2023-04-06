from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "SHF"
    addresses_name = "2023-05-04/2023-03-20T15:52:31.211109/Eros_SQL_Output009.csv"
    stations_name = "2023-05-04/2023-03-20T15:52:31.211109/Eros_SQL_Output009.csv"
    elections = ["2023-05-04"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "100052101093",  # BROOKFIELD, LONG LANE, STANNINGTON, SHEFFIELD
            "100051016653",  # EDENFIELD, LONG LANE, STANNINGTON, SHEFFIELD
            "100052094057",  # HALLWOOD HOUSE, PENISTONE ROAD, CHAPELTOWN, SHEFFIELD
            "10013646160",  # THE BUNGALOW, HALLWOOD, PENISTONE ROAD, CHAPELTOWN, SHEFFIELD
            "10022924822",  # 3 WADSLEY LANE, SHEFFIELD
            "100052186977",  # 3 BURTON STREET, SHEFFIELD
            "100052083193",  # WOODCLIFFE HOUSE, WOODCLIFFE, SHEFFIELD
            "100052081136",  # 59 CLARKEHOUSE ROAD, SHEFFIELD
            "100050950378",  # 5 CRUMMOCK ROAD, SHEFFIELD
            "100051115573",  # 5 WOODSEATS ROAD, SHEFFIELD
            "10094515334",  # FLAT, ABOVE 649-651, CHESTERFIELD ROAD, SHEFFIELD
            "10091734040",  # 165B BIRLEY SPA LANE, SHEFFIELD
            "10091734039",  # 165A BIRLEY SPA LANE, SHEFFIELD
            "100051088863",  # KNOWLE HILL, STREETFIELDS, HALFWAY, SHEFFIELD
            "10003573833",  # GROUNDS PLUS, UNIT 6 LONG ACRE WAY, SHEFFIELD
            "10023151677",  # 8A SOUTHEY GREEN ROAD, SHEFFIELD
        ]:
            return None

        if record.housepostcode in [
            # split
            "S8 0PL",
            "S10 3GW",
            "S36 2QF",
            "S1 4TA",
            "S10 3LG",
            "S35 9XS",
        ]:
            return None

        return super().address_record_to_dict(record)
