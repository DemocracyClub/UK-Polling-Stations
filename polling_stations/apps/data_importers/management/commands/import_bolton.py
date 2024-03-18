from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BOL"
    addresses_name = (
        "2024-05-02/2024-03-18T14:48:49.155147/Democracy_Club__02May2024.CSV"
    )
    stations_name = (
        "2024-05-02/2024-03-18T14:48:49.155147/Democracy_Club__02May2024.CSV"
    )
    elections = ["2024-05-02"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10070916825",  # CURLEYS FISHERY, TOP O TH WALLSUCHES, HORWICH, BOLTON
            "100012431797",  # 321 DERBY STREET, BOLTON
            "100012556511",  # 152 LONGSIGHT, BOLTON
            "10001244221",  # FLAT 1 290 ST HELENS ROAD, BOLTON
            "10001241112",  # ROOF TOP BARN, WINGATES LANE, WESTHOUGHTON, BOLTON
            "100012434531",  # RALPH FOLD COTTAGE, WINGATES LANE, WESTHOUGHTON, BOLTON
            "10001245228",  # METHODIST CHURCH DICCONSON LANE, ASPULL, BOLTON
            "100012558543",  # PARFEN LIMITED, SUNNYSIDE NURSING HOME ADELAIDE STREET, BOLTON
            "200002544033",  # 2 CUTACRE LANE, BOLTON
            "100012430429",  # ROYAL HOTEL, 142 ALBERT ROAD, FARNWORTH, BOLTON
            "100012430421",  # HOBOKEN HOUSE, AINSWORTH AVENUE, HORWICH, BOLTON
            "100012552065",  # HOLIDAY INN BOLTON, 1 HIGHER BRIDGE STREET, BOLTON
            "100010918636",  # 659 RADCLIFFE ROAD, BOLTON
            "100012434106",  # HILLSIDE FARM, TOTTINGTON ROAD, BOLTON
        ]:
            return None

        if record.addressline6 in [
            # splits
            "BL4 8JA",
            "BL6 4ED",
            "BL4 0LW",
            "BL1 2JU",
            "BL5 2DL",
            "BL1 5HP",
            "BL3 2DP",
            "BL3 3JY",
            "BL2 4JU",
            "BL1 3SJ",
            "BL1 2HZ",
            # looks wrong
            "BL5 2DJ",
            "BL3 2QH",
            "BL1 2HE",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # add postcode for: The One Stop Shop, Bolton Town Hall, Le Mans Crescent, Bolton
        if record.polling_place_id == "5573":
            record = record._replace(polling_place_postcode="BL1 1RJ")

        # add postcode for: The Triangle Annexe, Chorley Old Road
        if record.polling_place_id == "5758":
            record = record._replace(polling_place_postcode="BL1 5QP")

        # add postcode for: St Thomas CE Primary School, Eskrick Street
        if record.polling_place_id == "5792":
            record = record._replace(polling_place_postcode="BL1 3JB")

        # add postcode for: Ucan Centre (Former Tonge Moor Library), Tonge Moor Road
        if record.polling_place_id == "5544":
            record = record._replace(polling_place_postcode="BL2 2LE")

        # add postcode for: Hilton Community Centre, Nuttall Avenue
        if record.polling_place_id == "5688":
            record = record._replace(polling_place_postcode="BL6 5RA")

        # add postcode for: Chorley New Rd Primary School, Chorley New Road
        if record.polling_place_id == "5691":
            record = record._replace(polling_place_postcode="BL6 6EW")

        # add postcode for: The Pavilion, Doe Hey Park, Cawdor Avenue
        if record.polling_place_id == "5646":
            record = record._replace(polling_place_postcode="BL4 7HX")

        # add postcode for: Prestolee CP School, Church Road
        if record.polling_place_id == "5656":
            record = record._replace(polling_place_postcode="M26 1HJ")

        # add postcode for: Waggon Road Children's Centre, Waggon Road
        if record.polling_place_id == "5532":
            record = record._replace(polling_place_postcode="BL2 5AB")

        # add postcode for: Blackrod Community Centre (Rivington Room), Community Centre, Vicarage Road
        if record.polling_place_id == "5684":
            record = record._replace(polling_place_postcode="BL6 5AB")

        # add postcode for: Mobile Station, Cross Street
        if record.polling_place_id == "5784":
            record = record._replace(polling_place_postcode="BL1 2SQ")

        # add postcode for: Community Centre, Roosevelt Road
        if record.polling_place_id == "5655":
            record = record._replace(polling_place_postcode="BL4 8EA")

        # add postcode for: Mobile Station At Knutshaw Crescent
        if record.polling_place_id == "5734":
            record = record._replace(polling_place_postcode="BL3 4SB")

        # add postcode for: Drummond Street Community Centre, Drummond Street
        if record.polling_place_id == "5481":
            record = record._replace(polling_place_postcode="BL1 6QQ")

        return super().station_record_to_dict(record)
