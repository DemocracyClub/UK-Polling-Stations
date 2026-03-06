from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SHN"
    addresses_name = (
        "2026-05-07/2026-02-18T09:56:09.315370/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-02-18T09:56:09.315370/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # station change from council
        # OLD: SKK Judo Club Viaduct Street Newton le Willows WA12 9NH
        # NEW: St John the Baptists C of E Church, St John Street, Newton le Willows, WA12 9NW
        if record.polling_place_id == "6421":
            record = record._replace(
                polling_place_uprn="39055770",
                polling_place_easting="357296",
                polling_place_northing="395397",
                polling_place_name="St John the Baptists C of E Church",
                polling_place_address_1="St John Street",
                polling_place_postcode="WA12 9NW",
            )
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.post_code in [
            # split
            "WA10 1HT",
            "WA9 3RR",
        ]:
            return None
        return super().address_record_to_dict(record)
