from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SST"
    addresses_name = "2021-03-31T12:26:09.080338/South Staffs Democracy Club Report.csv"
    stations_name = "2021-03-31T12:26:09.080338/South Staffs Democracy Club Report.csv"
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100031812029",  # 7 PARK CLOSE, CHESLYN HAY, WALSALL, WS6 7DA
            "10003692636",  # NARROWBOAT SERENITY GAILEY WHARF WATLING STREET, GAILEY ST19 5PR
            "100031799992",  # GREENSFORGE HOUSE, GREENSFORGE, KINGSWINFORD, DY6 0AH
            "200004524554",  # IVETSEY BANK FARM, IVETSEY BANK, WHEATON ASTON, STAFFORD
            "10094875300",  # POOL FARM BUNGALOW, GAILEY LEA LANE, GAILEY, STAFFORD ST19 5PT
        ]:
            return None

        if record.addressline6 in [
            "ST19 9AB",
            "ST19 9AG",
            "WV8 1QS",
            "WV9 5BW",
            "ST19 5QH",
            "WS6 7BL",
            "WV11 2DN",
            "DY7 5EF",
            "WV5 9BN",
            "DY6 0BA",
            "WV5 7EY"
            #         "DY7 5HL",
            #         "ST19 5RH",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Bede Hall, Wombourne Parish Offices, Giggetty Lane, Wombourne, WV5 9EZ => WV5 9ED
        if record.polling_place_id == "4059":
            record = record._replace(polling_place_postcode="WV5 9ED")

        # Bishopswood Village Hall, Ivetsey Bank Road, Bishopswood, Stafford, ST19 9AR => ST19 9AB
        if record.polling_place_id == "3833":
            record = record._replace(polling_place_postcode="ST19 9AB")

        # Village Hall, High Street, Wheaton Aston, South Staffordshire ST19 9PL => ST19 9NG
        if record.polling_place_id == "3868":
            record = record._replace(polling_place_postcode="ST19 9NG")

        # Village Hall, Hyde Lea
        if record.polling_place_id == "3849":
            record = record._replace(
                polling_place_easting="391056", polling_place_northing="319891"
            )

        # St Bartholomews Church Hall
        if record.polling_place_id == "4044":
            record = record._replace(
                polling_place_easting="389364", polling_place_northing="295314"
            )

        return super().station_record_to_dict(record)
