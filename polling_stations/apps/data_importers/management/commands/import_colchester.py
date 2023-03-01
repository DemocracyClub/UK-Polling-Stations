from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "COL"
    addresses_name = (
        "2023-05-04/2023-03-01T16:36:55.674350/Democracy_Club__04May2023.csv"
    )
    stations_name = (
        "2023-05-04/2023-03-01T16:36:55.674350/Democracy_Club__04May2023.csv"
    )
    elections = ["2023-05-04"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10093741447",  # 84A MALDON ROAD, TIPTREE, COLCHESTER
            "10095444509",  # 2A BELLE VUE ROAD, WIVENHOE, COLCHESTER
            "10095443897",  # RUNKINS FARM LANGHAM LANE, BOXTED
            "10070226639",  # NORTON HALL, BOARDED BARN ROAD, WAKES COLNE, COLCHESTER
            "10034897228",  # THE SWEEPS, FOXES LANE, EIGHT ASH GREEN, COLCHESTER
            "100091238419",  # LAUREL COTTAGE, BIRCH STREET, BIRCH, COLCHESTER
            "100091472547",  # 88A COGGESHALL ROAD, MARKS TEY
            "100090464972",  # 148 MERSEA ROAD, COLCHESTER
            "10070237642",  # HOME FARM BUNGALOW CLINGOE HILL, COLCHESTER
            "10024406006",  # FERRY PRINCE, KING EDWARD QUAY, HYTHE QUAY, COLCHESTER
            "10004952417",  # 275A HARWICH ROAD, COLCHESTER
            "303008703",  # THE BUNGALOW, ERNULPH WALK, COLCHESTER
            "303001667",  # DRAGONFLY DAY NURSERY LTD, 14 NORTH HILL, COLCHESTER
            "100091472547",  # 88A COGGESHALL ROAD, MARKS TEY
            "303000247",  #  THE ROWS, CHURCH ROAD, LAYER-DE-LA-HAYE, COLCHESTER
            "10004948804",  # ROUND BUSH FARM, ROUNDBUSH ROAD, LAYER MARNEY, COLCHESTER
            "100091239138",  # OWLSTREE HOUSE, CHURCH LANE, STANWAY, COLCHESTER
            "100091241024",  # EAST LODGE, GUN HILL, DEDHAM, COLCHESTER
            "10093740679",  # MFV74 KING EDWARD QUAY, COLCHESTER
        ]:
            return None

        rec = super().address_record_to_dict(record)

        if record.addressline6 in [
            "CO4 3GQ",  # across another area; very close to another station
            "CO3 8ND",  # 1 - 5 CROSSBILLS WALK, STANWAY, COLCHESTER
            "CO5 9XE",  # PALMERS FARM, LAYER MARNEY, COLCHESTER and CLARKES, LAYER MARNEY, COLCHESTER
            "CO4 3SE",  # 1- 2 COLLIERS FARM COTTAGES, ELMSTEAD ROAD, COLCHESTER
            "CO4 3ZP",  # NEW PARK ANNEXE, CLINGOE HILL, COLCHESTER
            # splits
            "CO3 8DP",
            "CO4 5LG",
            "CO2 8BU",
            "CO6 1HA",
        ]:
            return None

        return rec

    def station_record_to_dict(self, record):
        # 'Paxman Academy, Paxman Avenue, Colchester, Essex, CO2 9DQ' (id: 12176)
        if record.polling_place_id == "12176":
            record = record._replace(polling_place_postcode="CO2 9DB")

        # 'Old Heath Community Centre, D`Arcy Road, Old Heath, Colchester, CO2 8BB' (id: 12106)
        if record.polling_place_id == "12106":
            record = record._replace(polling_place_postcode="CO2 8BA")

        return super().station_record_to_dict(record)
