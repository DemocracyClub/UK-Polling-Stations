from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "THE"
    addresses_name = (
        "2024-07-04/2024-05-31T10:30:11.205463/Democracy_Club__04July2024 (7).tsv"
    )
    stations_name = (
        "2024-07-04/2024-05-31T10:30:11.205463/Democracy_Club__04July2024 (7).tsv"
    )
    elections = ["2024-07-04"]
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
            "WD19 4LS",
            "WD3 6AB",
        ]:
            return None
        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Coates Way School, Coates Way, Garston, Watford, WD25 9NW (id: 6026)
        if record.polling_place_id == "6026":
            record = record._replace(polling_place_postcode="")
        return super().station_record_to_dict(record)
