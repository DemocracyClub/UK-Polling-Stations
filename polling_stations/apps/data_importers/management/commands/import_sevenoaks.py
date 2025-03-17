from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SEV"
    addresses_name = (
        "2025-05-01/2025-03-17T09:28:03.019684/Democracy_Club__01May2025 (1).tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-17T09:28:03.019684/Democracy_Club__01May2025 (1).tsv"
    )
    elections = ["2025-05-01"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # St. John`s Church Hall, Quakers Hall Lane, Sevenoaks TN13 3NU
        if record.polling_place_id == "10102":
            record = record._replace(
                polling_place_easting="553197",
                polling_place_northing="156100",
            )

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100061006745",  # STANWELL HOUSE, BOTSOM LANE, WEST KINGSDOWN, SEVENOAKS
            "10094320762",  # 1 THE VIEW, BOTSOM LANE, WEST KINGSDOWN, SEVENOAKS
            "50002013131",  # HIGH WOOD, BOTSOM LANE, WEST KINGSDOWN, SEVENOAKS
            "100062544307",  # 1 PUMPING STATION, SAINTS HILL, PENSHURST, TONBRIDGE
            "100062544308",  # 2 PUMPING STATION, SAINTS HILL, PENSHURST, TONBRIDGE
        ]:
            return None
        return super().address_record_to_dict(record)
