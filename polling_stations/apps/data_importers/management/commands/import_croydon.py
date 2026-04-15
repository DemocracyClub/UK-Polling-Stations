from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CRY"
    addresses_name = (
        "2026-05-07/2026-02-05T13:28:59.885856/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-02-05T13:28:59.885856/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # station change from council
        # OLD: Start-Up Croydon, Weatherill House, 23 Whitestone Way, Croydon, CR0 4WF
        # NEW: Temporary Polling Station, Car Park, M&S Purley Cross, 330 Purley Way, Croydon CR0 4XJ
        if record.polling_place_id == "17965":
            record = record._replace(
                polling_place_name="Temporary Polling Station",
                polling_place_address_1="M&S Car Park",
                polling_place_address_2="Purley Cross",
                polling_place_address_3="330 Purley Way",
                polling_place_address_4="Croydon",
                polling_place_postcode="CR0 4XJ",
            )

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100020676357",  # 18A CROHAM ROAD, SOUTH CROYDON
            "10093049200",  # 16 LIMPSFIELD ROAD, SOUTH CROYDON
            "10093049201",  # 16A LIMPSFIELD ROAD, SOUTH CROYDON
            "10093049201",  # 16A LIMPSFIELD ROAD, SOUTH CROYDON
            "200001221192",  # 141 BRIGHTON ROAD, PURLEY
            "10014054732",  # 97 NOVA ROAD, CROYDON
            "10014054731",  # 95 NOVA ROAD, CROYDON
            "10094493457",  # 44 COOMBE ROAD, CROYDON
            "100020690731",  # 39 BRICKFIELD ROAD, THORNTON HEATH
            "100020584917",  # WEST LODGE, BISHOPS WALK, CROYDON
        ]:
            return None

        if record.addressline6 in [
            # looks wrong
            "SE19 3FB",
            "CR8 3ES",
            "CR5 3NY",
            "CR3 5QQ",
            "CR2 0FP",
        ]:
            return None

        return super().address_record_to_dict(record)
