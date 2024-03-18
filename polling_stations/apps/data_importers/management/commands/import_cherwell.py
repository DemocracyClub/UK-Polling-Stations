from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CHR"
    addresses_name = "2024-05-02/2024-03-18T10:37:12.510808/Cherwell DC - Democracy_Club__02May2024.tsv"
    stations_name = "2024-05-02/2024-03-18T10:37:12.510808/Cherwell DC - Democracy_Club__02May2024.tsv"
    elections = ["2024-05-02"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10011890176",  # WITHYCOMBE FARMHOUSE, STRATFORD ROAD, DRAYTON, BANBURY
            "10011888678",  # ARDLEY BOARDING KENNELS, BARN HOUSE, ARDLEY, BICESTER
            "10011938272",  # THE OLD MILK SHED LANGFORD PARK FARM LONDON ROAD, BICESTER
            "10011938385",  # FLAT AT 75 HIGH STREET, BANBURY
            "10011918678",  # FLAT AT 45 HIGH STREET, BANBURY
            "10011889660",  # THE BUNGALOW, THE SHADES, BANBURY
        ]:
            return None

        if record.addressline6 in [
            # splits
            "OX16 5AW",
            "OX27 7AE",
            "OX26 3EB",
            "OX26 3EZ",
            # looks wrong
            "OX16 1EU",
            "OX16 2SX",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # correct point for: The Church of St John the Baptist, Broadway, Kidlington, Oxon
        if record.polling_place_id == "28492":
            record = record._replace(polling_place_easting="449651")
            record = record._replace(polling_place_northing="212578")

        # add missing postcode for: Heyford Park Community Centre, Brice Road, Upper Heyford
        if record.polling_place_id == "28530":
            record = record._replace(polling_place_postcode="OX25 5TF")

        return super().station_record_to_dict(record)
