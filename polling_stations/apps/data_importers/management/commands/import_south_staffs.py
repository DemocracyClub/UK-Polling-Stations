from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SST"
    addresses_name = (
        "2021-03-23T12:44:29.340168/South Staffs Democracy_Club__06May2021.CSV"
    )
    stations_name = (
        "2021-03-23T12:44:29.340168/South Staffs Democracy_Club__06May2021.CSV"
    )
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
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
            "DY7 5HL",
            "ST19 5RH",
            "ST19 9AG",
            "WV9 5BW",
            "WV11 2DN",
        ]:
            return None

        return rec

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
