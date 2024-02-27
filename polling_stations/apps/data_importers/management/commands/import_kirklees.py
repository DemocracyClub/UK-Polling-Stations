from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "KIR"
    addresses_name = (
        "2024-05-02/2024-02-07T16:49:27.870935/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-02-07T16:49:27.870935/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Cleckheaton Methodist Church, Greenside Cleckheaton
        if record.polling_place_id == "17890":
            record = record._replace(polling_place_easting="419000")
            record = record._replace(polling_place_northing="425200")

        # Roberttown Community Centre - Entrance is on Church Rd
        if record.polling_place_id == "18240":
            record = record._replace(polling_place_easting="419480")
            record = record._replace(polling_place_northing="422649")

        # fix from council:
        # OLD: Dewsbury Town Hall, Ground Floor Registrar Communal Area, Wakefield Old Road, Dewsbury
        # NEW: Dewsbury Town Hall, Ground Floor (main reception), Wakefield Old Road, Dewsbury
        if record.polling_place_id == "19028":
            record = record._replace(
                polling_place_address_1="Ground Floor (main reception)"
            )

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
            "83183588",  # 1 HARE PARK LANE, LIVERSEDGE
            "83108387",  # GROVE LODGE, SHIRLEY VILLAS, RAWFOLDS, CLECKHEATON
            "83146894",  # 15 PARK GATE, SKELMANTHORPE, HUDDERSFIELD
            "83146906",  # THE BARN, PARK GATE, SKELMANTHORPE, HUDDERSFIELD
            "83157946",  # HIGHBRIDGE LODGE, HIGHBRIDGE, SCISSETT, HUDDERSFIELD
            "83189002",  # CAUSEWAY FOOT, OUTLANE, HUDDERSFIELD
            "83234731",  # 2A SOUTHLANDS DRIVE, FIXBY, HUDDERSFIELD
        ]:
            return None

        if record.addressline6 in [
            # split
            "HD8 9ZD",
            "HD5 8EE",
            # suspect
            "WF15 6JS",
            "WF14 8EB",
            "HD4 7BD",
            "HD2 2NH",
            "HD8 0LQ",
        ]:
            return None

        return super().address_record_to_dict(record)
