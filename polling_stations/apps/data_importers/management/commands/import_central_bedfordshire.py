from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):

    council_id = "CBF"
    addresses_name = "2021-03-16T16:10:23.712198/Democracy_Club__06May2021.CSV"
    stations_name = "2021-03-16T16:10:23.712198/Democracy_Club__06May2021.CSV"
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def station_record_to_dict(self, record):
        # Haynes Village Hall Northwood End Road Haynes Beds MK45 3QB
        if record.polling_place_id == "14700":
            record = record._replace(polling_place_easting="510086")
            record = record._replace(polling_place_northing="242021")

        # Flitton Church Hall Brook Lane Flitton Beds MK45 5EJ - removing misleading point
        if record.polling_place_id == "14663":
            record = record._replace(polling_place_easting="")
            record = record._replace(polling_place_northing="")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100080999932",  # 4 BREWERS HILL ROAD, DUNSTABLE
            "10094352855",  # 11 STRATTON, MARSTON MORETAINE, BEDFORD
            "10094352856",  # 12 BREWERS HILL ROAD, DUNSTABLE
            "10094352858",  # 10 BREWERS HILL ROAD, DUNSTABLE
            "10014618845",  # 6 BREWERS HILL ROAD, DUNSTABLE
            "10094352859",  # 8 BREWERS HILL ROAD, DUNSTABLE
            "10094352857",  # 2 BREWERS HILL ROAD, DUNSTABLE
            "100081002043",  # 2A BREWERS HILL ROAD, DUNSTABLE
            "10094352860",  # 12A BREWERS HILL ROAD, DUNSTABLE
            "10094352854",  # LONDON LODGE, WOBURN, MILTON KEYNES
            "10094352861",  # PARK FARM, HAZELWOOD LANE, AMPTHILL, BEDFORD
            "100081002361",  # THE BUTTERFLY, GREAT NORTH ROAD, SANDY
        ]:
            return None

        if record.addressline6 in [
            "SG18 8GF",
            "SG5 4PS",
            "SG18 9TA",
            "LU6 3NB",
            "MK45 1QX",
            "SG18 8JD",
            "MK45 1XL",
            "SG18 9SY",
            "MK45 1AX",
            "SG18 0JL",
            "MK45 1QZ",
            "MK45 1JA",
            "LU7 4AY",
        ]:
            return None

        return super().address_record_to_dict(record)
