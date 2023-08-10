from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WRL"
    addresses_name = (
        "2023-05-04/2023-02-22T10:54:17.531032/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-02-22T10:54:17.531032/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Marlowe Road URC Hall
        if record.polling_place_id in ["10084", "10088"]:
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-3.050648, 53.417306, srid=4326)
            return rec

        # user issue report #87
        # The Grange Public House
        if record.polling_place_id == "10254":
            rec = super().station_record_to_dict(record)
            rec["location"] = Point(-3.122875, 53.396797, srid=4326)
            return rec

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "42004030",  # GREEN COTTAGE, ARROWE PARK ROAD, WIRRAL
            "42194110",  # CHARTWELL GAYTON STABLES CHESTER ROAD, GAYTON
            "42205031",  # 227A HOYLAKE ROAD, WIRRAL
            "42177133",  # LOVELL PARTNERSHIP LTD, MARKETING SUITE 497 BOROUGH ROAD, OXTON
            "42068483",  # 4 LORNE ROAD, PRENTON
            "42205588",  # 105 GROVE ROAD, WALLASEY
            "42005155",  # TOP FLOOR FLAT 9 ATHERTON STREET, NEW BRIGHTON"# ,
            "42192662",  # FRANKBY HALL FRANKBY CEMETERY MONTGOMERY HILL, FRANKBY
        ]:
            return None

        if record.addressline6 in [
            "CH42 0HD",
            "CH62 7FE",
            "CH62 7FE",
            "CH62 7FE",
            "CH49 3PG",
            "CH49 2SE",
            "CH62 8AB",
            "CH42 9PD",
        ]:
            return None

        return super().address_record_to_dict(record)
