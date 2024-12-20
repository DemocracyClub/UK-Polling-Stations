from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "DEB"
    addresses_name = (
        "2024-07-04/2024-06-13T15:32:42.310608/Democracy Club - Polling Districts.csv"
    )
    stations_name = (
        "2024-07-04/2024-06-13T15:32:42.310608/Democracy Club - Polling Stations.csv"
    )
    elections = ["2024-07-04"]

    def station_record_to_dict(self, record):
        # Station coordinates change requested by council
        # MATLOCK - FARMERS VIEW, WITHIN HURST FARM SOCIAL CLUB, HAZEL GROVE, MATLOCK, DERBYSHIRE, DE4 3ED
        if record.pollingstationid == "3026":
            record = record._replace(xordinate="430853", yordinate="360507")

        # Removes polling stations name duplication in addresses
        record = record._replace(add1="")

        # Removes empty stations from cross-boundary constituencies
        try:
            if int(record.stationcode) >= 89:
                return None
        except ValueError:
            pass

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if (
            uprn
            in [
                "10070109674",  # FOREST LANE FARM, TIDESWELL MOOR, TIDESWELL, BUXTON
                "10070088354",  # PEACH LODGE, FOOLOW, EYAM, HOPE VALLEY
                "10070107940",  # 5 THE WOODLANDS, THORNBRIDGE, GREAT LONGSTONE, BAKEWELL
                "10070089739",  # 37 PARK ROAD, BAKEWELL
                "10070106848",  # CONKSBURY FARM, CONKSBURY, BAKEWELL
                "10070078911",  # NEWHAVEN COTTAGE FARM, HARTINGTON, BUXTON
                "10010338116",  # BOSKIN COTTAGE, GRANGE MILL, MATLOCK
                "10070075658",  # 1 BAILEYS CLOSE, PARK LANE, RODSLEY, ASHBOURNE
                "10070102595",  # HOLLIES FARM, MARSTON COMMON, MARSTON MONTGOMERY, ASHBOURNE
                "10070087915",  # BRICK HILL COTTAGE, HOLLINGTON LANE, EDNASTON, ASHBOURNE
                "10070103452",  # 109 WELLINGTON STREET, MATLOCK
                "10010337873",  # SPINNEYFORD BROOK COTTAGE, NORTH LANE, BRAILSFORD, ASHBOURNE
                "10070077968",  # BENTFIELD, ASHBOURNE ROAD, SUDBURY, ASHBOURNE
                "10070077967",  # LODGE COTTAGE, ASHBOURNE ROAD, SUDBURY, ASHBOURNE
                "10070088693",  # KEEPERS COTTAGE, PIKEHALL, MATLOCK
                "10070079847",  # NEW VINCENT FARM, PARSLEY HAY, BUXTON
                "10010337127",  # GREEN VIEW FARM, PIKEHALL, MATLOCK
                "10070088497",  # LEACROFT, PARWICH LANE, PIKEHALL, MATLOCK
                "10070083303",  # BANK HOUSE, WYASTON ROAD, ASHBOURNE
                "10010337013",  # FLAT ABOVE DUKE OF YORK UNNAMED SECTION OF A515 BETWEEN TAGG LANE AND DISTRICT
                "10010341175",  # FLAT, BULL IN THE THORN, FLAGG, BUXTON
                "10070082942",  # 3 WOODLANDS COTTAGES, STURSTON, ASHBOURNE
                "10070082941",  # THE WOODLANDS, STURSTON, ASHBOURNE
                "10070083989",  # WOODLAKE, BRADLEY, ASHBOURNE
                "10070082149",  # BRIDGE COTTAGE, SHIRLEY COMMON, SHIRLEY, ASHBOURNE
                "10070077964",  # 2 COTONWOOD COTTAGE, ASHBOURNE ROAD, SUDBURY, ASHBOURNE
                "10070077965",  # 1 COTONWOOD COTTAGE, ASHBOURNE ROAD, SUDBURY, ASHBOURNE
                "10010344035",  # 9 OLD METHODIST CHURCH, BANK ROAD, MATLOCK
            ]
        ):
            return None

        if record.postcode in [
            "DE6 2AR",  # split
            # suspect
            "DE6 1AR",  # MAYFIELD ROAD, ASHBOURNE
            "DE4 51JQ",  # ASHBOURNE ROAD, MONYASH, BAKEWELL
            "DE6 5PE",  # SOMERSAL HERBERT, ASHBOURNE
        ]:
            return None

        return super().address_record_to_dict(record)
