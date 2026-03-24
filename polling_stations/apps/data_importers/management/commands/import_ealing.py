from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "EAL"
    addresses_name = "2026-05-07/2026-03-24T14:55:25.345777/EC Democracy_Club__07May2026 Polling Station Lookup.tsv"
    stations_name = "2026-05-07/2026-03-24T14:55:25.345777/EC Democracy_Club__07May2026 Polling Station Lookup.tsv"
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "12147146",  # 35A PRIORY GARDENS, LONDON
            "12181729",  # FLAT 3 55 PARK AVENUE, PARK ROYAL
            "12181728",  # FLAT 2 55 PARK AVENUE, PARK ROYAL
            "12181730",  # FLAT 4 55 PARK AVENUE, PARK ROYAL
            "12181731",  # FLAT 5 55 PARK AVENUE, PARK ROYAL
            "12096646",  # TRAVELODGE HOTELS LTD, 614 WESTERN AVENUE, LONDON
        ]:
            return None
        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # The postcode for the following station has been confirmed by the council:
        # West London University Sports Pavilion, (Home of Pitshanger Football Club), Argyle Road, W13 8EL

        return super().station_record_to_dict(record)
