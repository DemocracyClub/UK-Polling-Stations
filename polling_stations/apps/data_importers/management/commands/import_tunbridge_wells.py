from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "TUN"
    addresses_name = (
        "2026-05-07/2026-02-10T13:29:01.152535/Democracy_Club__07May2026 - 10Feb.tsv"
    )
    stations_name = (
        "2026-05-07/2026-02-10T13:29:01.152535/Democracy_Club__07May2026 - 10Feb.tsv"
    )
    elections = ["2026-05-07"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    # Ignore warnings about addressbase postcode for below stations - council decision:
    # - St Barnabas Hall, Quarry Road, Tunbridge Wells
    # - The Hub, Grosvenor Recreation Ground, Auckland Road, Royal Tunbridge Wells
    # - St James Church Hall, St James Road, Royal Tunbridge Wells
    # - St Mark`s Hall, Bayham Road, Royal Tunbridge Wells
    # - The Library, Number One Community Centre, Rowan Tree Road, Tunbridge Wells

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100062544084",  # COURTYARD FLAT, COLEBROOKE, PEMBURY ROAD, TONBRIDGE
            "100062543933",  # COLEBROOKE HOUSE, PEMBURY ROAD, TONBRIDGE
            "100061193913",  # HUNTERS LODGE, PEMBURY ROAD, TONBRIDGE
            "100062551952",  # BLACK BUSH COTTAGE, BEDGEBURY ROAD, GOUDHURST, Cranbrook
            "10090055018",  # CRABTREE HOUSE, COURSE HORN LANE, CRANBROOK
            "10008666136",  # NIGHTINGALE COTTAGE, CONGHURST LANE, HAWKHURST, CRANBROOK
            "100062543979",  # 1 BROOK FARM COTTAGES, FIVE OAK GREEN ROAD, TONBRIDGE
        ]:
            return None

        if record.addressline6 in [
            # split
            "TN3 0HX",
            "TN4 0AB",
            # suspect
            "TN12 7BZ",
        ]:
            return None

        return super().address_record_to_dict(record)
