from django.contrib.gis.geos import Point
from data_importers.management.commands import (
    BaseXpressDCCsvInconsistentPostcodesImporter,
)


class Command(BaseXpressDCCsvInconsistentPostcodesImporter):
    council_id = "DOR"
    addresses_name = "2021-03-04T13:35:03.539800/Democracy_Club__06May2021.tsv"
    stations_name = "2021-03-04T13:35:03.539800/Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"
    # There have been a lot of fixes, so try letting rest through.

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10002059554",  # EAST BARN, WOOTTON FITZPAINE, BRIDPORT
            "10002639052",  # WEST BARN, WOOTTON FITZPAINE, BRIDPORT
            "100040632406",  # 3 CONINGSBY PLACE, POUNDBURY
            "100041117551",  # WARDENS CARAVAN SEAVIEW HOLIDAY PARK PRESTON ROAD, WEYMOUTH
            "10013012017",  # 4 CANN COURT, BUTTS KNAPP, SHAFTESBURY
            "100040632405",  # 3 CANN COURT, BUTTS KNAPP, SHAFTESBURY
            "100040620232",  # 1 CANN COURT, BUTTS KNAPP, SHAFTESBURY
            "10002643131",  # 2 CANN COURT, BUTTS KNAPP, SHAFTESBURY
            "200000753878",  # THE PRESBYTERY, CULLIFORD ROAD NORTH, DORCHESTER
            "10093508099",  # FLAT 3, 3A VICKERY COURT, POUNDBURY, DORCHESTER
            "10093508100",  # POPPY BANK FARM HIGHER STREET, OKEFORD FITZPAINE
            "200000767496",  # ICEN BARN, GRANGE ROAD, WAREHAM
            "200000767497",  # OAKS 1 HERSTON YARD CAMPSITE WASHPOND LANE, HERSTON, SWANAGE
            "10002641794",  # 21A EAST STREET, CORFE CASTLE, WAREHAM
            "100040644451",  # 11 BUTTS KNAPP, SHAFTESBURY
            "10023248033",  # YARD FARM, PILSDON, BRIDPORT
            "200000768680",  # THE OLD CIDER PRESS, EAST STREET, BEAMINSTER
            "10023250031",  # 1 ANGEL COTTAGES LONG ASH LANE, WARDON HILL
            "10093510179",  # COCKWELL FARM, MORCOMBELAKE, BRIDPORT
            "100041115108",  # CLEAR VIEW, MARTINSTOWN, DORCHESTER
            "10023242607",  # GRAYS FARM, CLIFT LANE, TOLLER PORCORUM, DORCHESTER
            "10013291491",  # STATION LODGE, HOLYWELL, DORCHESTER
            "10013293094",  # SHERBORNE SCHOOL FOR GIRLS, ALDHELMSTED EAST HOUSE, BRADFORD ROAD, SHERBORNE
            "10013293093",  # GRAYS FARMHOUSE, CLIFT LANE, TOLLER PORCORUM, DORCHESTER
            "10013293091",  # BOAR COTTAGE, CLIFT LANE, TOLLER PORCORUM, DORCHESTER
            "10013293092",  # GRAYS COTTAGE CLIFT LANE, TOLLER PORCORUM
            "10013297602",  # THE DOVE HOUSE, GRANGE ROAD, WAREHAM
            "10013297222",  # CORFE WAY, VALLEY ROAD, SWANAGE
            "10071152307",  # THE OLD COFFEE SHOP, WARDON HILL, DORCHESTER
            "200001871356",  # "2 COCKWELL FARMHOUSE TIZARD'S KNAP, MORCOMBELAKE"
            "200004826761",  # BRACKEN COTTAGE, EAST BURTON ROAD, WOOL, WAREHAM
            "10013733675",  # FLAT, LYTCHETT HEATH, LYTCHETT HEATH, POOLE
            "100041048946",  # FLAT, 30A SALISBURY STREET, BLANDFORD FORUM
            "100041099139",  # THE COURTYARD CRAFT CENTRE, HUNTICK ROAD, LYTCHETT MINSTER, POOLE
            "10011954350",  # 5 HIGHER COMMON, CHILD OKEFORD, BLANDFORD FORUM
            "100041231992",  # LITTLE RIDGE, WATERSTON, DORCHESTER
            "200004827276",  # HEWISH FARM, FRIAR WADDON, WEYMOUTH
            "10023251192",  # MOBILE HOME BIRCH YARD RYE WATER LANE, CORSCOMBE
        ]:
            return None

        if record.addressline6 in [
            "DT4 0BA",
            "DT4 7QN",
            "DT3 6SD",
            "DT6 4QH",
            "DT6 6EU",
            "DT6 4LD",
            "DT2 0JE",
            "DT9 5FP",
            "DT2 8DX",
            "SP7 8RE",
            "SP8 4AL",
            "SP8 4DG",
            "DT10 1HG",
            "DT10 1QZ",
            "BH21 7LY",
            "BH21 7BG",
            "BH21 2DE",
            "BH31 6PA",
            "BH21 3NF",
            "BH21 4AD",
            "BH31 6EH",
            "BH31 6QG",
            "BH21 5NP",
            "BH21 5JD",
            "BH21 4JU",
            "BH19 2PG",
            "BH20 5JJ",
            "BH20 4BJ",
            "BH20 5PT",
            "DT5 2FD",
            "DT3 4GF",
            "DT5 2FB",
            "DT2 8GD",
            "BH19 1BS",
            "BH19 1DQ",
        ]:
            return None

        rec = super().address_record_to_dict(record)

        if uprn in [
            "10013731266",  # FLAT 2 PURBECK LODGE 15 BONNETS LANE, WAREHAM
            "10013731265",  # FLAT 1 PURBECK LODGE 15 BONNETS LANE, WAREHAM
        ]:
            rec["postcode"] = "BH20 4HA"

        return rec

    def station_record_to_dict(self, record):

        if (
            "NEW LOCATION" in record.polling_place_name
        ):  # Multiple station address names contain undesired text
            record = record._replace(polling_place_name="")

        if (
            record.polling_place_id == "39510"
        ):  # Thorncombe Village Hall Chard Street Thorncombe TA20 4ME
            record = record._replace(polling_place_postcode="TA20 4NF")

        if (
            record.polling_place_id == "39843"
        ):  # St Marks Church Hall New Road West Parley Ferndown Dorset
            record = record._replace(polling_place_postcode="BH22 8EW")

        if (
            record.polling_place_id == "39899"
        ):  # Weymouth Outdoor Education Centre Knightsdale Road Weymouth DT4 OHS
            record = record._replace(polling_place_postcode="DT4 0HS")

        rec = super().station_record_to_dict(record)

        # Bishops Caundle Village Hall
        # user issue report #40
        if record.polling_place_id == "39641":
            rec["location"] = Point(-2.437757, 50.915554, srid=4326)

        return rec
