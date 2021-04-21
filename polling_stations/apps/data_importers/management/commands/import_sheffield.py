from django.contrib.gis.geos import Point
from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "SHF"
    addresses_name = "2021-04-06T12:06:39.850590/polling_station_export-2021-04-06.csv"
    stations_name = "2021-04-06T12:06:39.850590/polling_station_export-2021-04-06.csv"
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def station_record_to_dict(self, record):

        # St Mary's Walkley Community Hall Howard Road Sheffield S6 3EX
        if (
            record.pollingstationnumber == "199"
            and record.pollingstationpostcode == "S6 3EX"
        ):
            record = record._replace(pollingstationpostcode="")

        rec = super().station_record_to_dict(record)

        # user issue report #82
        if (
            rec
            and rec["internal_council_id"]
            == "116-hillsborough-trinity-methodist-church-lennox-rd-entrance"
        ):
            rec["location"] = Point(-1.504240, 53.408718, srid=4326)

        return rec

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "100050922015",  # BRACKENFIELDS, BLAND LANE, SHEFFIELD
            "200003021647",  # WHITE LODGE FARM, HIGH BRADFIELD, BRADFIELD, SHEFFIELD
            "100052101093",  # BROOKFIELD, LONG LANE, STANNINGTON, SHEFFIELD
            "100051016653",  # EDENFIELD, LONG LANE, STANNINGTON, SHEFFIELD
            "10013303341",  # SERVITE SISTERS, SERVITE CONVENT, PACK HORSE LANE, HIGH GREEN, SHEFFIELD
            "200003001575",  # THE BARN, ELLIOT LANE, GRENOSIDE, SHEFFIELD
            "200002997296",  # THE STABLES, ELLIOT LANE, GRENOSIDE, SHEFFIELD
            "100052094057",  # HALLWOOD HOUSE, PENISTONE ROAD, CHAPELTOWN, SHEFFIELD
            "10013646160",  # THE BUNGALOW, HALLWOOD, PENISTONE ROAD, CHAPELTOWN, SHEFFIELD
            "100050998359",  # MILLSTONE BARN, HIRST COMMON LANE, SHEFFIELD
            "10022924822",  # 3 WADSLEY LANE, SHEFFIELD
            "10091127976",  # OLD CROWN INN, MANAGERS ACCOMMODATION 710 PENISTONE ROAD, OWLERTON, SHEFFIELD
            "100052186977",  # 3 BURTON STREET, SHEFFIELD
            "10091129074",  # FAGANS, MANAGERS ACCOMMODATION 69 BROAD LANE, SHEFFIELD
            "100052083193",  # WOODCLIFFE HOUSE, WOODCLIFFE, SHEFFIELD
            "100052081136",  # 59 CLARKEHOUSE ROAD, SHEFFIELD
            "100050950378",  # 5 CRUMMOCK ROAD, SHEFFIELD
            "100051115573",  # 5 WOODSEATS ROAD, SHEFFIELD
            "10094515334",  # FLAT, ABOVE 649-651, CHESTERFIELD ROAD, SHEFFIELD
            "10091734040",  # 165B BIRLEY SPA LANE, SHEFFIELD
            "10091734039",  # 165A BIRLEY SPA LANE, SHEFFIELD
            "100051088863",  # KNOWLE HILL, STREETFIELDS, HALFWAY, SHEFFIELD
            "10003573833",  # GROUNDS PLUS, UNIT 6 LONG ACRE WAY, SHEFFIELD
        ]:
            return None

        if record.housepostcode in [
            "S10 3LG",
            "S10 3GW",
            "S8 0PL",
            "S35 2WW",
            "S35 2TQ",
            "S6 2BB",
            "S6 2BH",
            "S6 3ED",
            "S1 4AZ",
            "S13 7PP",
        ]:
            return None

        return super().address_record_to_dict(record)
