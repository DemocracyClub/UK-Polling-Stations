from django.contrib.gis.geos import Point

from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "SHF"
    addresses_name = (
        "2022-05-05/2022-03-28T12:49:20.231925/polling_station_export-2022-03-28.csv"
    )
    stations_name = (
        "2022-05-05/2022-03-28T12:49:20.231925/polling_station_export-2022-03-28.csv"
    )
    elections = ["2022-05-05"]

    def apply_council_station_corrections(self, record):
        # Has to be applied in both station and address methods, so that the generated station ID
        # is consistent.

        # Correction from council: https://trello.com/c/Od6Ski5i
        if record.pollingstationnumber in ("62"):
            record = record._replace(
                pollingstationname="Cabin on land adjacent to 4 Handsworth Avenue",
                pollingstationaddress_1="",
                pollingstationaddress_2="Sheffield",
                pollingstationpostcode="S9 4BT",
            )
        return record

    def station_record_to_dict(self, record):
        record = self.apply_council_station_corrections(record)

        # Laycock's Sports Club, Archer Road, Sheffield
        if record.pollingstationnumber == "109":
            record = record._replace(pollingstationpostcode="S8 0JZ")  # was S8 0JY

        rec = super().station_record_to_dict(record)

        # user issue report #82; wrong location is that of another station
        if (
            rec
            and rec["internal_council_id"]
            == "117-hillsborough-trinity-methodist-church-lennox-rd-entrance"
        ):
            rec["location"] = Point(-1.504240, 53.408718, srid=4326)

        return rec

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
            "S1 4TA",
            "S35 9XS",
            "S8 0PL",
            "S10 3GW",
            "S10 3LG",
        ]:
            return None

        record = self.apply_council_station_corrections(record)

        return super().address_record_to_dict(record)
