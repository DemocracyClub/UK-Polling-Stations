from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WRX"
    addresses_name = (
        "2026-05-07/2026-03-03T13:54:44.245422/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-03T13:54:44.245422/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10004522399",  # GRESFORD HALL, GRESFORD, WREXHAM
            "200002944484",  # ALYN VALE COTTAGE, MOLD ROAD, CEFN-Y-BEDD, WREXHAM
            "10023163146",  # 3 CROESNEWYDD ROAD, WREXHAM
            "10004513276",  # Y BWTHYN, LLWYNEINION, RHOSLLANERCHRUGOG, WREXHAM
            "200002944623",  # BRYN HOVAH, BANGOR ROAD, OVERTON, WREXHAM
            "200001649414",  # BRYN HOVAH HOUSE, OVERTON ROAD, BANGOR-ON-DEE, WREXHAM
            "200002944623",  # BRYN HOVAH, BANGOR ROAD, OVERTON, WREXHAM
        ]:
            return None

        if record.addressline6 in [
            # splits
            "LL12 8DH",
            "LL20 7HJ",
            "LL13 9EN",
            "LL13 9LW",
            "LL13 0YU",
            "SY13 3BU",
            "LL13 0JW",
            "LL13 8US",
            "LL11 4UY",
            "LL12 0RY",
            # looks wrong
            "LL11 3EZ",
            "LL14 5BG",
            "LL11 4TT",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # postcode correction for: Gresford Methodist Church Hall, Chester Road, Gresford, Wrexham, LL12 8YY
        if record.polling_place_id == "10770":
            record = record._replace(polling_place_postcode="LL12 8PA")

        # postcode correction for: Gwersyllt Congregational Church, 3 Dodds Lane, Gwersyllt, Wrexham, LL11 4LG
        # requested by the council
        if record.polling_place_id == "10808":
            record = record._replace(polling_place_postcode="LL11 4NT")

        return super().station_record_to_dict(record)
