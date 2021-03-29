from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "ENF"
    addresses_name = "2021-03-25T12:37:41.448482/Democracy_Club__06May2021.25.3.21.tsv"
    stations_name = "2021-03-25T12:37:41.448482/Democracy_Club__06May2021.25.3.21.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):

        # Enfield Highway Community Centre, 117 Hertford Road, Enfield
        if record.polling_place_id == "7447":
            record = record._replace(polling_place_easting="535189")
            record = record._replace(polling_place_northing="197091")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "207022171",  # FLAT 3, MICHAEL HOUSE 55-57, CHASE SIDE, LONDON
            "207019443",  # FLAT 2 39A CHURCH STREET, EDMONTON
            "207016774",  # FLAT 2 928 HERTFORD ROAD, ENFIELD
            "207012586",  # CAR WASH, REAR OF 18-22, STERLING WAY, LONDON
            "207017770",  # 293A HERTFORD ROAD, ENFIELD
            "207001778",  # 49 PRIVATE ROAD, ENFIELD
            "207022169",  # FLAT 1, MICHAEL HOUSE 55-57, CHASE SIDE, LONDON
            "207022173",  # FLAT 5, MICHAEL HOUSE 55-57, CHASE SIDE, LONDON
            "207022172",  # FLAT 4, MICHAEL HOUSE 55-57, CHASE SIDE, LONDON
            "207022170",  # FLAT 2, MICHAEL HOUSE 55-57, CHASE SIDE, LONDON
            "207180896",  # ST DAVIDS LODGE MILLFIELD COMPLEX SILVER STREET, EDMONTON
            "207019444",  # FLAT 3 39A CHURCH STREET, EDMONTON
            "207019442",  # FLAT 1 39A CHURCH STREET, EDMONTON
            "207024239",  # 371A NORTH CIRCULAR ROAD, SOUTHGATE
            "207015921",  # FRONT LODGE, TRENT PARK, COCKFOSTERS ROAD, BARNET
            "207013920",  # 6A BEECH HILL, BARNET
        ]:
            return None

        if record.addressline6 in [
            "EN2 9HJ",
            "N21 2DS",
            "N21 3AU",
            "N13 4RR",
            "EN2 9HN",
            "N9 9RP",
            "N18 2EH",
        ]:
            return None

        return super().address_record_to_dict(record)
