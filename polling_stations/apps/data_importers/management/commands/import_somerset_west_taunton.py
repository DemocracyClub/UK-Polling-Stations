from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SWT"
    addresses_name = (
        "2022-05-05/2022-04-07T15:17:08.822354/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-04-07T15:17:08.822354/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
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
            "10093895310",  # KILTON COTTAGES, 11 KILTON, HOLFORD, BRIDGWATER
            "10014267234",  # MOONBEAMS FARM, WELLINGTON
            "10008798191",  # PIXFORD FARM, BISHOPS LYDEARD, TAUNTON
            "10008799902",  # HIGHER BARN PIXFORD FRUIT FARM RALEIGHS CROSS ROAD, COMBE FLOREY, TAUNTON
            "10008799901",  # ROSE COTTAGE, KILTON, HOLFORD, BRIDGWATER
            "100041178433",  # SLADE TOWER, EIGHT ACRE LANE, WELLINGTON
        ]:
            return None

        if record.addressline6 in [
            "TA23 0ED",
            "TA2 8AX",
            "TA3 5FE",
            "TA23 0NX",
            "TA24 6TE",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Williams Hall Dark Lane Stoke St Gregory Taunton TA3 6HA
        if record.polling_place_id == "9376":
            record = record._replace(polling_place_easting="334829")
            record = record._replace(polling_place_northing="127291")

        # Victoria Park Pavilion Victoria Gate Taunton TA1 3ES
        if record.polling_place_id == "9272":
            record = record._replace(polling_place_easting="323519")
            record = record._replace(polling_place_northing="124839")

        return super().station_record_to_dict(record)
