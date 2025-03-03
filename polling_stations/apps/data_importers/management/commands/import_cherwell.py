from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CHR"
    addresses_name = (
        "2025-05-01/2025-03-03T15:42:51.074676/Democracy_Club__01May2025 (2).tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-03T15:42:51.074676/Democracy_Club__01May2025 (2).tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10011938272",  # THE OLD MILK SHED LANGFORD PARK FARM LONDON ROAD, BICESTER
            "10011938385",  # FLAT AT 75 HIGH STREET, BANBURY
            "10011918678",  # FLAT AT 45 HIGH STREET, BANBURY
        ]:
            return None

        if record.addressline6 in [
            # splits
            "OX26 3EB",
            "OX27 7AE",
            "OX16 5AW",
            "OX26 3EZ",
            # looks wrong
            "OX16 1EU",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # add missing postcode for: Heyford Park Community Centre, Brice Road, Upper Heyford
        if record.polling_place_id == "31314":
            record = record._replace(polling_place_postcode="OX25 5TF")

        return super().station_record_to_dict(record)
