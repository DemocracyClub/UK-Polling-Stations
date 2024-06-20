from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CRY"
    addresses_name = (
        "2024-07-04/2024-06-20T21:29:23.214180/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-20T21:29:23.214180/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100020676357",  # 18A CROHAM ROAD, SOUTH CROYDON
            "10094492830",  # 1A COVINGTON WAY, LONDON
            "10001006634",  # 3 LANSDOWNE PLACE, LONDON
            "100020642075",  # BASEMENT FLAT, 193 CHURCH ROAD, LONDON
            "100020642076",  # 193 CHURCH ROAD, LONDON
            "100020622449",  # 5A SHIRLEY OAKS ROAD, CROYDON
            "100020622448",  # 2 SHIRLEY OAKS ROAD, CROYDON
            "100020584917",  # WEST LODGE, BISHOPS WALK, CROYDON3
            "10093049200",  # 16 LIMPSFIELD ROAD, SOUTH CROYDON
            "10093049201",  # 16A LIMPSFIELD ROAD, SOUTH CROYDON
            "10093049201",  # 16A LIMPSFIELD ROAD, SOUTH CROYDON
            "100020635515",  # 260 HAYES LANE, KENLEY
            "200001221192",  # 141 BRIGHTON ROAD, PURLEY
            "100020593700",  # 49 CROWLEY CRESCENT, CROYDON
            "10014054732",  # 97 NOVA ROAD, CROYDON
            "10014054731",  # 95 NOVA ROAD, CROYDON
            "10094493457",  # 44 COOMBE ROAD, CROYDON
            "10093046375",  # 237A SYDENHAM ROAD, CROYDON
            "10093756168",  # FLAT 1, 80 WADDON NEW ROAD, CROYDON
            "10093756169",  # FLAT 2, 80 WADDON NEW ROAD, CROYDON
            "100020688674",  # 56 WEST HILL, SOUTH CROYDON
        ]:
            return None

        if record.addressline6 in [
            # splits
            "CR0 2JB",
            "CR0 4BF",
            "CR2 0JB",
            "SE25 4BA",
            # looks wrong
            "SE19 3FB",
            "CR2 8JT",
            "CR2 0RW",
            "CR8 5AR",
            "CR8 3ES",
        ]:
            return None

        return super().address_record_to_dict(record)
