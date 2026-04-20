from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "COL"
    addresses_name = (
        "2026-05-07/2026-03-16T12:39:16.036477/Democracy_Club__07May2026.CSV"
    )
    stations_name = (
        "2026-05-07/2026-03-16T12:39:16.036477/Democracy_Club__07May2026.CSV"
    )
    elections = ["2026-05-07"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "10070229236",  # COLCHESTER FABRICATIONS, THE SWALLOWS, WORMINGFORD ROAD, FORDHAM, COLCHESTER, CO6 3NS
                "100091472547",  # SIMPLE VAN HIRE, 88A COGGESHALL ROAD, MARKS TEY, COLCHESTER, CO6 1LS
                "10034898298",  # MERVILLE BARRACKS, POST ROOM, CIRCULAR ROAD SOUTH, COLCHESTER, CO2 7UT
                "10095444509",  # 2A BELLE VUE ROAD, WIVENHOE, COLCHESTER, CO7 9LE
                "10095445911",  # 32D MAYPOLE GREEN ROAD, COLCHESTER, CO2 9NX
                "10095443897",  # RUNKINS FARM, LANGHAM LANE, BOXTED, COLCHESTER
            ]
        ):
            return None

        if record.post_code in [
            # splits
            "CO4 5LG",
            "CO2 8BU",
            "CO6 1HA",
            # looks wrong
            "CO4 3ZP",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # changes requested by council (missing UPRNs and coordinates)
        # data correction for: St Cedd`s Church Hall, Iceni Way, Colchester, CO2 9BZ
        if record.polling_place_id == "14536":
            record = record._replace(
                polling_place_postcode="CO2 9EH",
                polling_place_easting="597790",
                polling_place_northing="223225",
                polling_place_uprn="10004965578",
            )
        # add missing data for: Aldham Village Hall, Tey Road, Aldham, Colchester, CO6 3RB
        if record.polling_place_id == "14368":
            record = record._replace(
                polling_place_easting="591699",
                polling_place_northing="225838",
                polling_place_uprn="303005757",
            )

        # add missing data for: Chappel & Wakes Colne Village Hall, Colchester Road, Wakes Colne, Colchester, CO6 2BX
        if record.polling_place_id == "14372":
            record = record._replace(
                polling_place_easting="589422",
                polling_place_northing="228582",
                polling_place_uprn="100091625670",
            )

        # add missing data for: Church of Jesus Christ of Latter Day Saints, 272 Straight Road, Colchester, CO3 9DX
        if record.polling_place_id == "14272":
            record = record._replace(
                polling_place_easting="596737",
                polling_place_northing="223633",
                polling_place_uprn="10004964484",
            )

        # add missing data for: Easthorpe Church Hall, Easthorpe Road, Easthorpe, Colchester, CO5 9HD
        if record.polling_place_id == "14440":
            record = record._replace(
                polling_place_easting="591266",
                polling_place_northing="221514",
                polling_place_uprn="10034899287",
            )

        # add missing data for: Little Horkesley Village Hall, School Lane, School Road, Little Horkesley, Colchester, CO6 4DJ
        if record.polling_place_id == "14360":
            record = record._replace(
                polling_place_easting="595929",
                polling_place_northing="232104",
                polling_place_uprn="303005879",
            )

        # add missing data for: Messing Village Hall, The Street, Messing, Colchester, CO5 9TR
        if record.polling_place_id == "14458":
            record = record._replace(
                polling_place_easting="589636",
                polling_place_northing="218945",
                polling_place_uprn="10004955624",
            )

        # add missing data for: Mount Bures Village Hall, Craigs Lane, Mount Bures, Bures, CO8 5AN
        if record.polling_place_id == "14380":
            record = record._replace(
                polling_place_easting="590570",
                polling_place_northing="232698",
                polling_place_uprn="10004951443",
            )

        # add missing data for: Quaker Meeting House, 6 Church Street, Colchester, CO1 1NF
        if record.polling_place_id == "14313":
            record = record._replace(
                polling_place_easting="599320",
                polling_place_northing="225080",
                polling_place_uprn="10004945075",
            )

        # add missing data for: St. Margaret`s Church Hall, Stansted Road, Colchester, CO2 8RA
        if record.polling_place_id == "14187":
            record = record._replace(
                polling_place_easting="600304",
                polling_place_northing="222358",
                polling_place_uprn="10004964366",
            )

        # add missing data for: Tiptree United Reformed Church Hall, Chapel Road, Tiptree, CO5 0HP
        if record.polling_place_id == "14504":
            record = record._replace(
                polling_place_easting="590310",
                polling_place_northing="216090",
                polling_place_uprn="10070236494",
            )

        return super().station_record_to_dict(record)
