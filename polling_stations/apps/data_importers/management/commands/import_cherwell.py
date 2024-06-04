from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CHR"
    addresses_name = "2024-07-04/2024-06-10T14:52:42.069384/combined.tsv"
    stations_name = "2024-07-04/2024-06-10T14:52:42.069384/combined.tsv"
    elections = ["2024-07-04"]
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
        # add missing postcode for: Heyford Park Community Centre, Brice Road, Upper Heyford
        if record.polling_place_id == "30098":
            record = record._replace(polling_place_postcode="OX25 5TF")

        return super().station_record_to_dict(record)
