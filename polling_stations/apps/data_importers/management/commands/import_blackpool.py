from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BPL"
    addresses_name = (
        "2021-04-16T09:25:32.153684/BLACKPOOL COUNCIL Democracy_Club__06May2021.CSV"
    )
    stations_name = (
        "2021-04-16T09:25:32.153684/BLACKPOOL COUNCIL Democracy_Club__06May2021.CSV"
    )
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10000109140",  # 1 WINDMILL MOBILE HOME PARK PRESTON NEW ROAD, BLACKPOOL
            "10070846645",  # FLAT 3 38 VANCE ROAD, BLACKPOOL
            "10000109123",  # FLAT 3 481 WATERLOO ROAD, BLACKPOOL
            "100012858457",  # 45 TYLDESLEY ROAD, BLACKPOOL
            "10070843907",  # DELLTON, 9 GROSVENOR STREET, BLACKPOOL
            "10070847268",  # 89A HOLMFIELD ROAD, BLACKPOOL
            "10070849351",  # GROUND FLOOR FLAT 5 HOLMFIELD ROAD, BLACKPOOL
        ]:
            return None

        if record.addressline6 in ["FY1 5DE", "FY4 1HU"]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # South Shore Lawn Tennis Club Midgeland Road Blackpool FY4 4HZ
        if record.polling_place_id == "5789":
            record = record._replace(polling_place_postcode="")

        return super().station_record_to_dict(record)
