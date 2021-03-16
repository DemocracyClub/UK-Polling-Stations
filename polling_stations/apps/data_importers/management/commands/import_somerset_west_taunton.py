from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SWT"
    addresses_name = "2021-03-15T10:53:03.510333/Somerset Democracy_Club__06May2021.CSV"
    stations_name = "2021-03-15T10:53:03.510333/Somerset Democracy_Club__06May2021.CSV"
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10003766236",  # WEBBS WEST, DULVERTON
            "10003766237",  # WEBBS EAST, DULVERTON
            "10023836744",  # BARN COTTAGE MARSHCLOSE HILL, WITHYPOOL
            "200003156693",  # 3A PARKHOUSE ROAD, MINEHEAD
            "10003561537",  # FLAT C, MILLBRIDGE COURT, 11 PARKHOUSE ROAD, MINEHEAD
            "10003561536",  # FLAT B, MILLBRIDGE COURT, 11 PARKHOUSE ROAD, MINEHEAD
            "10003561538",  # FLAT D, MILLBRIDGE COURT, 11 PARKHOUSE ROAD, MINEHEAD
            "200003156566",  # 9A PARKHOUSE ROAD, MINEHEAD
            "10003561535",  # FLAT A, MILLBRIDGE COURT, 11 PARKHOUSE ROAD, MINEHEAD
            "100040960688",  # 9B PARKHOUSE ROAD, MINEHEAD
            "100040960686",  # 7 PARKHOUSE ROAD, MINEHEAD
            "100040960685",  # OVERS, PARKHOUSE ROAD, MINEHEAD
            "200003156694",  # 3B PARKHOUSE ROAD, MINEHEAD
            "10003561539",  # FLAT E, MILLBRIDGE COURT, 11 PARKHOUSE ROAD, MINEHEAD
            "10003561540",  # FLAT F, MILLBRIDGE COURT, 11 PARKHOUSE ROAD, MINEHEAD
            "10003766053",  # HARPFORD HOUSE, PAYTON, WELLINGTON
            "10003764036",  # HARPFORD BARN, PAYTON, WELLINGTON
            "10093895310",  # KILTON COTTAGES, 11 KILTON, HOLFORD, BRIDGWATER
            "10014267234",  # MOONBEAMS FARM, WELLINGTON
            "10008799902",  # HIGHER BARN PIXFORD FRUIT FARM RALEIGHS CROSS ROAD, COMBE FLOREY, TAUNTON
            "10008799901",  # ROSE COTTAGE, KILTON, HOLFORD, BRIDGWATER
            "100041178433",  # SLADE TOWER, EIGHT ACRE LANE, WELLINGTON
            "10023836286",  # MARSHWOOD, EXTON, DULVERTON
            "10008799958",  # POTTERS COTTAGE, WEST MONKTON, TAUNTON
        ]:
            return None

        if record.addressline6 in ["TA3 5FE", "TA23 0NX", "TA23 0ED", "TA24 6TE"]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Elworthy Monksilver & Nettlecombe Community Hall Combe Cross Hill Monksilver Taunton TA4 4JR
        if record.polling_place_id == "8791":
            record = record._replace(polling_place_postcode="TA4 4JE")

        # Wellington Rugby Club Corams Lane Wellington TA21 8JA
        if record.polling_place_id == "9017":
            record = record._replace(polling_place_postcode="TA21 8LL")

        # Williams Hall Dark Lane Stoke St Gregory Taunton TA3 6HA
        if record.polling_place_id == "8865":
            record = record._replace(polling_place_easting="334829")
            record = record._replace(polling_place_northing="127291")

        # Victoria Park Pavilion Victoria Gate Taunton TA1 3ES
        if record.polling_place_id == "8915":
            record = record._replace(polling_place_easting="323519")
            record = record._replace(polling_place_northing="124839")

        return super().station_record_to_dict(record)
