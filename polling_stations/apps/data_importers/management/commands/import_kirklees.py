from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "KIR"
    addresses_name = (
        "2026-05-07/2026-01-28T13:18:41.550999/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-01-28T13:18:41.550999/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Roberttown Community Centre - Entrance is on Church Rd
        if record.polling_place_id == "22518":
            record = record._replace(polling_place_easting="419480")
            record = record._replace(polling_place_northing="422649")

        # Removing bad coordinates for:
        # Broad Oak Bowling Club, 73 Broad Oak, Cowlersley Lane, Linthwaite, Huddersfield, HD7 5TE
        if record.polling_place_id == "22238":
            record = record._replace(polling_place_easting="410268")
            record = record._replace(polling_place_northing="414480")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "83190068",  # 5 MOOR TOP FARM, MOOR TOP LANE, FLOCKTON MOOR, WAKEFIELD
            "83183588",  # 1 HARE PARK LANE, LIVERSEDGE
            "83157946",  # HIGHBRIDGE LODGE, HIGHBRIDGE, SCISSETT, HUDDERSFIELD
            "83050605",  # 67 GLENEAGLES WAY, HUDDERSFIELD
            "83050604",  # 69 GLENEAGLES WAY, HUDDERSFIELD
            "83050607",  # 71 GLENEAGLES WAY, HUDDERSFIELD
        ]:
            return None

        if record.addressline6 in [
            # split
            "WF17 7ND",
        ]:
            return None

        return super().address_record_to_dict(record)
