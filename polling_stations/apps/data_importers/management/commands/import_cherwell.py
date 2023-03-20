from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CHR"
    addresses_name = (
        "2023-05-04/2023-03-20T16:46:19.346211/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-20T16:46:19.346211/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10011889761",  # ANNEXE ADJACENT 2 LANGFORD COTTAGES LONDON ROAD, BICESTER
            "100121291839",  # LANGFORD PARK FARM HOUSE, LONDON ROAD, BICESTER
            "10011906163",  # PICKED PIECE CORNER, BANBURY ROAD, SHIPTON-ON-CHERWELL, KIDLINGTON
            "10011937037",  # NARROWBOAT BUDE SCHOOL LANE, CROPREDY
            "10011935665",  # FLAT 4, THE COURTS, WARWICK ROAD, BANBURY
            "10011890176",  # WITHYCOMBE FARMHOUSE, STRATFORD ROAD, DRAYTON, BANBURY
            "100121287994",  # PINEWOOD COTTAGE, SIBFORD ROAD, SHUTFORD, BANBURY
            "10011898079",  # 237 HEYFORD PARK, CAMP ROAD, UPPER HEYFORD, BICESTER
            "10011888678",  # ARDLEY BOARDING KENNELS, BARN HOUSE, ARDLEY, BICESTER
            "10011889217",  # WRETCHWICK LODGE, AYLESBURY ROAD, BICESTER
            "10011921025",  # 129 LEACH ROAD, BICESTER
        ]:
            return None

        if record.addressline6 in [
            # splits
            "OX27 7AE",
            "OX16 9QF",
            "OX26 3EB",
            "OX5 1LZ",
            "OX26 3EZ",
            "OX16 5AW",
            "OX25 5BH",  # ALLEN ROW, EADY ROAD, UPPER HEYFORD, BICESTER
            "OX16 1EU",  # LONGELANDES CLOSE, BANBURY
            "OX16 2SX",  # WHARF COTTAGES, SOUTHAM ROAD, BANBURY
            "OX26 6HB",  # LONDON ROAD, BICESTER
            "OX5 2BP",  # ASHDOWN HOUSE, OXFORD ROAD, KIDLINGTON
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # The Church of St John the Baptist, Broadway, Kidlington, Oxon
        if record.polling_place_id == "26602":
            record = record._replace(polling_place_easting="449651")
            record = record._replace(polling_place_northing="212578")

        # Heyford Park Community Centre, Brice Road, Upper Heyford
        if record.polling_place_id == "26587":
            record = record._replace(polling_place_postcode="OX25 5TF")

        return super().station_record_to_dict(record)
