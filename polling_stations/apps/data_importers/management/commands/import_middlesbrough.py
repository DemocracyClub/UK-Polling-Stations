from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MDB"
    addresses_name = (
        "2024-05-02/2024-03-07T15:17:39.494958/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-07T15:17:39.494958/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
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
        # adding point for: Mobile Station - Hemlington Grange Way, Junction of Ravengill Road, Middlesbrough, TS8 9FX
        if record.polling_place_id == "9713":
            record = record._replace(polling_place_easting="450225")
            record = record._replace(polling_place_northing="514104")

        # adding point for: Mobile Station - Medina Gardens, Junction of Medina Gardens and Acklam Road, TS5 8BN
        if record.polling_place_id == "9694":
            record = record._replace(polling_place_easting="449116")
            record = record._replace(polling_place_northing="515625")

        # adding point for: St. Chad`s Church Hall, Keith Road, Middlesbrough, TS5 7QW
        if record.polling_place_id == "9804":
            record = record._replace(polling_place_easting="449587")
            record = record._replace(polling_place_northing="517743")

        return super().station_record_to_dict(record)
