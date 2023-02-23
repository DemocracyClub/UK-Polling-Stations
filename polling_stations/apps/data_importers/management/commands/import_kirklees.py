from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "KIR"
    addresses_name = (
        "2023-05-04/2023-02-23T07:24:43.333519/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-02-23T07:24:43.333519/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Cleckheaton Methodist Church, Greenside Cleckheaton
        if record.polling_place_id == "16365":
            record = record._replace(polling_place_easting="")
            record = record._replace(polling_place_northing="")

        # Roberttown Community Centre - Entrance is on Church Rd
        if record.polling_place_id == "16722":
            record = record._replace(polling_place_easting="419480")
            record = record._replace(polling_place_northing="422649")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200003798867",  # IVY COTTAGE, CUMBERWORTH, HUDDERSFIELD
            "83188196",  # HEY LEYS, MARSDEN LANE, SLAITHWAITE, HUDDERSFIELD
            "83172558",  # THE LODGE, HOSTINGLEY LANE, THORNHILL, DEWSBURY
            "83197512",  # THE BARN, TOP YARD, BOG GREEN LANE, HUDDERSFIELD
            "83089738",  # HOLLY COTTAGE BOG GREEN LANE, COLNE BRIDGE, HUDDERSFIELD
            "83124543",  # 153 LINFIT LANE, KIRKBURTON, HUDDERSFIELD
            "83170159",  # TOPPIT COTTAGE, BAGDEN LANE, CLAYTON WEST, HUDDERSFIELD
            "83190068",  # 5 MOOR TOP FARM, MOOR TOP LANE, FLOCKTON MOOR, WAKEFIELD
            "83197513",  # 310 BOG GREEN LANE, HUDDERSFIELD
        ]:
            return None

        if record.addressline6 in [
            "HD9 7EH",
        ]:
            return None

        return super().address_record_to_dict(record)
