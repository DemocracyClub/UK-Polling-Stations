from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BNH"
    addresses_name = (
        "2024-05-02/2024-02-19T10:29:56.065905/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-02-19T10:29:56.065905/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "22031382",  # COURT FARM HOUSE COURT FARM DEVIL'S DYKE ROAD, HOVE
            "22175494",  # THE LODGE, BRIGHTON RACE COURSE, FRESHFIELD ROAD, BRIGHTON
            "22272586",  # 1 GREEN MEWS, 53 HOGARTH ROAD, HOVE
            "22272587",  # 2 GREEN MEWS, 53 HOGARTH ROAD, HOVE
            "22272588",  # 3 GREEN MEWS, 53 HOGARTH ROAD, HOVE
            "22279648",  # 184C PORTLAND ROAD, HOVE
            "22057837",  # 260 LONDON ROAD, PRESTON, BRIGHTON
            "22057280",  # 90 PEACOCK LANE, BRIGHTON
        ]:
            return None

        if record.addressline6 in [
            # split
            "BN1 8NF",
            "BN2 9PA",
            "BN1 3AE",
            "BN1 9BW",  # 1 DENMAN PLACE, BRIGHTON
            "BN4 12PL",  # MILE OAK ROAD, PORTSLADE, BRIGHTON
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Change requested by the council
        # Old station: The Spire, St Mark`s Chapel, Eastern Road, Brighton, BN2 5JN (id: 15585)
        # Replaced by: T.S.Nautilus, 39A Chesham Road, BN2 1NB
        if record.polling_place_id == "15585":
            record = record._replace(polling_place_name="T.S. Nautilus")
            record = record._replace(polling_place_address_1="39A Chesham Road")
            record = record._replace(polling_place_address_2="")
            record = record._replace(polling_place_address_3="")
            record = record._replace(polling_place_address_4="")
            record = record._replace(polling_place_postcode="BN2 1NB")
            record = record._replace(polling_place_easting="533010")
            record = record._replace(polling_place_northing="103609")

        return super().station_record_to_dict(record)
