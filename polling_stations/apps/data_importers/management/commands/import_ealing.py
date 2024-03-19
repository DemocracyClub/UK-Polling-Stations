import re

from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "EAL"
    addresses_name = (
        "2024-05-02/2024-03-19T10:22:00.536492/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-19T10:22:00.536492/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "12180637",  # ANNEXE 20 LOCARNO ROAD, GREENFORD
            "12147146",  # 35A PRIORY GARDENS, LONDON
            "12181729",  # FLAT 3 55 PARK AVENUE, PARK ROYAL
            "12181728",  # FLAT 2 55 PARK AVENUE, PARK ROYAL
            "12181730",  # FLAT 4 55 PARK AVENUE, PARK ROYAL
            "12181731",  # FLAT 5 55 PARK AVENUE, PARK ROYAL
        ]:
            return None

        if record.addressline6 in [
            "W4 5HL",  # split
        ]:
            return None
        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Incomplete postcodes for temporary stations
        if re.match(r"^[A-Z]{1,2}[0-9]{1,2}$", record.polling_place_postcode):
            record = record._replace(polling_place_postcode="")
        return super().station_record_to_dict(record)
