from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "PEN"
    addresses_name = "2021-03-22T11:55:12.927152/Pendle Democracy_Club__06May2021.tsv"
    stations_name = "2021-03-22T11:55:12.927152/Pendle Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Rolls Royce Leisure, Skipton Road, Barnoldswick BB18 5RU
        if record.polling_place_id == "4117":
            record = record._replace(polling_place_postcode="BB18 6HJ")

        # Thomas Street Bowling Pavilion, Percy Street, Nelson BB9 9AY
        if record.polling_place_id == "4099":
            record = record._replace(
                polling_place_postcode="BB9 9BZ",
                polling_place_northing=437261,
                polling_place_easting=386085,
            )

        # Baptist School Guilford Street Brierfield BB9 5LH - moving postcode to correct place
        if record.polling_place_id == "4106":
            record = record._replace(
                polling_place_postcode=record.polling_place_address_3
            )
            record = record._replace(polling_place_address_3="")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10090962922",  # THE CHALET SANSBURY FARM SOUTHFIELD LANE, SOUTHFIELD
            "10090962921",  # THE BUNGALOW SANSBURY FARM SOUTHFIELD LANE, SOUTHFIELD
            "100012400513",  # FLAT 3, REEDYFORD COTTAGE, SCOTLAND ROAD, NELSON
            "100012400515",  # FLAT 5, REEDYFORD COTTAGE, SCOTLAND ROAD, NELSON
            "100012400512",  # FLAT 2, REEDYFORD COTTAGE, SCOTLAND ROAD, NELSON
            "100012400514",  # FLAT 4, REEDYFORD COTTAGE, SCOTLAND ROAD, NELSON
            "100012400511",  # FLAT 1, REEDYFORD COTTAGE, SCOTLAND ROAD, NELSON
        ]:
            return None

        if record.addressline6 in ["BB9 0RQ", "BB8 7JP", "BB8 0JR"]:
            return None

        return super().address_record_to_dict(record)
