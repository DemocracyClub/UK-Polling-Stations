from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "THE"
    addresses_name = (
        "2025-05-01/2025-03-06T09:55:19.565747/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-06T09:55:19.565747/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")
        if uprn in [
            "200000937007",  # OAK COTTAGE, HIGH ROAD, LEAVESDEN, WATFORD
            "200000937008",  # WAYSIDE, HIGH ROAD, LEAVESDEN, WATFORD
        ]:
            return None
        if record.addressline6 in [
            # split
            "WD3 6AB",
            "WD19 4LS",
        ]:
            return None
        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Council confirmed postcode for:
        # Coates Way School, Coates Way, Garston, Watford, WD25 9NW (id: 6026)
        return super().station_record_to_dict(record)
