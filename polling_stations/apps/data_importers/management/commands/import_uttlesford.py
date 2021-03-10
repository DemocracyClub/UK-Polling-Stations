from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "UTT"
    addresses_name = "2021-03-09T11:57:50.428803/Democracy_Club__06May2021_UDC.CSV"
    stations_name = "2021-03-09T11:57:50.428803/Democracy_Club__06May2021_UDC.CSV"
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200004270735",  # "THE BARN, PLEDGDON GREEN, HENHAM, BISHOP'S STORTFORD"
            "10002182834",  # ANNEXE AT PLEDGDON LODGE BRICK END ROAD, HENHAM
            "200004261749",  # B LODGE, EASTON LODGE, LITTLE EASTON, DUNMOW
            "100091278781",  # GREENWOOD, CHURCH ROAD, CHRISHALL, ROYSTON
            "10090833371",  # NEW FARM ARKESDEN ROAD, WENDENS AMBO
            "100091276459",  # 6 CHICKNEY ROAD, HENHAM, BISHOP'S STORTFORD
            "100091277104",  # ARCHWAYS OLD MEAD ROAD, HENHAM
        ]:
            return None

        if record.addressline6 in ["CM22 6FG", "CM22 6TW"]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # St. Mary`s CoE Foundation Primary School, Stansted School Hall Hampton Road Stansted CM24 8FE
        if record.polling_place_id == "688":
            record = record._replace(polling_place_uprn="10090833547")

        # R A Butler School, R A Butler Academy - School Hall, South Road, Saffron Walden
        if record.polling_place_id == "676":
            record = record._replace(polling_place_uprn="200004267358")

        # Chrishall New Village Hall Crawley End Chrishall Royston SG8 8QJ
        if record.polling_place_id == "637":
            record = record._replace(polling_place_uprn="200004259626")

        # Ashdon Village Hall Radwinter Road Ashdon Saffron Walden
        if record.polling_place_id == "547":
            record = record._replace(polling_place_postcode="CB10 2HA")

        # Removing postcodes where council data is incorrect or inconclusive
        if record.polling_place_id in [
            "552",  # Hadstock Village Hall,  Church Lane, Hadstock
            "556",  # Sewards End Village Hall,  Radwinter Road, Sewards End, Saffron Walden
            "565",  # Hatfield Heath Village Hall,  The Heath, Hatfield Heath, Bishop`s Stortford
            "577",  # Langley Community Centre,  Langley Upper Green, Saffron Walden
            "584",  # The Community Hall at Carver Barracks,  Off Elder Street, Wimbish, Saffron Walden
            "587",  # Wimbish Village Hall,  Tye Green, Wimbish, Saffron Walden
            "621",  # Hatfield Broad Oak Village Hall,  Cage End, Hatfield Broad Oak, Bishop`s Stortford
            "632",  # Leaden Roding Village Hall,  Stortford Road,  Leaden Roding,  Dunmow
            "642",  # Elmdon Village Hall,  Cross Hill, Elmdon, Saffron Walden
            "668",  # Council Offices,  London Road,  London Road, Saffron Walden, Essex
            "685",  # St. Mary`s Church Hall,  Birchanger Lane, Birchanger, Bishops Stortford
            "694",  # Farnham Village Hall,  Rectory Lane, Farnham, Bishop`s Stortford
            "702",  # Broxted Village Hall,  Browns End Road, Broxted, Dunmow
            "704",  # Little Canfield Village Hall,  Stortford Road, Little Canfield, Dunmow
            "707",  # Mole Hill Green Village Hall,  Mole Hill Green, Takeley, Bishop`s Stortford
            "718",  # Great Easton Village Hall,  Rebecca Meade, Great Easton, Dunmow
        ]:
            record = record._replace(polling_place_postcode="")

        return super().station_record_to_dict(record)
