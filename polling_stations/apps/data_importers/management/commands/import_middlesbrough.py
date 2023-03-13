from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "MDB"
    addresses_name = (
        "2023-05-04/2023-03-13T11:24:05.406792/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-13T11:24:05.406792/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200001683756",  # 220A LINTHORPE ROAD, MIDDLESBROUGH
            "10023181276",  # THE GRANARY, STAINSBY HALL FARM, THORNABY, STOCKTON-ON-TEES
            "10023174667",  # FLAT CAPTAIN COOK HOTEL 7-11 DURHAM STREET, MIDDLESBROUGH
            "10023181276",  # FLAT 1 169 BOROUGH ROAD, MIDDLESBROUGH
            "200000259465",  # 220A LINTHORPE ROAD, MIDDLESBROUGH
            "100110140269",  # 30 THORNFIELD ROAD, MIDDLESBROUGH
            "100110140271",  # 32 THORNFIELD ROAD, MIDDLESBROUGH
            "100110109926",  # 44 FALKLAND STREET, MIDDLESBROUGH
            "10093978798",  # FLAT 5 73 BOROUGH ROAD, MIDDLESBROUGH
            "10093978797",  # FLAT 4 73 BOROUGH ROAD, MIDDLESBROUGH
            "10023175713",  # FLAT NAVIGATION INN MARSH ROAD, MIDDLESBROUGH
        ]:
            return None

        if record.addressline6 in [
            "TS5 5EG",  # splits
            "TS1 3QD",  # VICTORIA ROAD, MIDDLESBROUGH
            "TS1 4AD",  # 27 BOROUGH ROAD, MIDDLESBROUGH
            "TS1 4AG",  # 149 LINTHORPE ROAD, MIDDLESBROUGH
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Mobile Station - Hemlington Grange Way, Junction of Ravensgill Road, Middlesbrough
        if record.polling_place_id == "9525":
            record = record._replace(polling_place_easting="")
            record = record._replace(polling_place_northing="")

        return super().station_record_to_dict(record)
