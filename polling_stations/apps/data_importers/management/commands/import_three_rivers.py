from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "THE"
    addresses_name = (
        "2026-05-07/2026-03-24T11:55:44.867070/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-24T11:55:44.867070/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
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
        # WARNING: Polling station Coates Way School is in Watford Borough Council (WAT)
        # WARNING: Polling station Leavesden Green is in Watford Borough Council (WAT)
        # addresses and locations are correct, just across the council border

        # wrong uprn for: Coates Way School, Coates Way, Garston, Watford, WD25 9NW
        if record.polling_place_id == "6990":
            record = record._replace(polling_place_uprn="")

        # wrong uprn for: Hillside Centre, Hillside Road, Chorleywood, Rickmansworth, WD3 5AP
        if record.polling_place_id == "6939":
            record = record._replace(polling_place_uprn="")

        return super().station_record_to_dict(record)
