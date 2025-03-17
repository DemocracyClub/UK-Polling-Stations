from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "TUN"
    addresses_name = (
        "2025-05-01/2025-03-17T16:00:04.636176/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-17T16:00:04.636176/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
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
        ]:
            return None

        if record.addressline6 in [
            # split
            "TN4 0AB",
            "TN3 0HX",
            # suspect
            "TN11 0PG",
            "TN18 5AH",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # UPRN correction from council for: Kilndown Village Hall, Church Road, Kilndown, Cranbrook, Kent, TN17 2RY
        if record.polling_place_id == "4303":
            record = record._replace(polling_place_uprn="10008671449")

        # UPRN correction from council for: The Function Room, The Hawkhurst Club Unity Hall, TN18 4AG
        if record.polling_place_id == "4289":
            record = record._replace(
                polling_place_uprn="100062553029",
                polling_place_easting="",
                polling_place_northing="",
            )
        return super().station_record_to_dict(record)
