from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MDB"
    addresses_name = (
        "2024-07-04/2024-05-28T09:46:41.092607/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-05-28T09:46:41.092607/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200001683756",  # 220A LINTHORPE ROAD, MIDDLESBROUGH
            "10023181276",  # THE GRANARY, STAINSBY HALL FARM, THORNABY, STOCKTON-ON-TEES
            "10023181276",  # FLAT 1 169 BOROUGH ROAD, MIDDLESBROUGH
            "200000259465",  # 220A LINTHORPE ROAD, MIDDLESBROUGH
            "100110109926",  # 44 FALKLAND STREET, MIDDLESBROUGH
            "10093978798",  # FLAT 5 73 BOROUGH ROAD, MIDDLESBROUGH
            "10093978797",  # FLAT 4 73 BOROUGH ROAD, MIDDLESBROUGH
            "10023175713",  # FLAT NAVIGATION INN MARSH ROAD, MIDDLESBROUGH
            "10023176944",  # FLAT 1, 27 BOROUGH ROAD, MIDDLESBROUGH
            "100110104313",  # 64 CROFT AVENUE, MIDDLESBROUGH
            "100110120765",  # 29 LEVICK CRESCENT, MIDDLESBROUGH
            "100110113890",  # 1 GROVE ROAD, MIDDLESBROUGH
            "100110095666",  # 163 BOROUGH ROAD, MIDDLESBROUGH
            "100110105569",  # 69 DEEPDALE AVENUE, MIDDLESBROUGH
        ]:
            return None

        if record.addressline6 in [
            # splits
            "TS5 5EG",
            # looks wrong
            "TS1 3QD",
            "TS1 4AG",
            "TS1 2PX",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # adding point for: St. Chad`s Church Hall, Keith Road, Middlesbrough, TS5 7QW
        if record.polling_place_id == "10001":
            record = record._replace(polling_place_easting="449587")
            record = record._replace(polling_place_northing="517743")

        # Corrections from council:
        # old: Mobile Station - Northern Road, Northern Road, Middlesbrough, TS5 4NS
        # new: Mobile Station - Junction of Northern Road and Acklam Road, Northern Road, Middlesbrough, TS5 4NS
        if record.polling_place_id == "9912":
            record = record._replace(
                polling_place_name="Mobile Station - Junction of Northern Road and Acklam Road",
                polling_place_easting="448012",
                polling_place_northing="518686",
            )

        return super().station_record_to_dict(record)
