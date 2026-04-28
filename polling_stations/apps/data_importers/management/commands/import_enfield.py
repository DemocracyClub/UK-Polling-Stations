from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "ENF"
    addresses_name = (
        "2026-05-07/2026-04-28T10:00:19.619113/Democracy_Club__07May2026 - 27-4-26.tsv"
    )
    stations_name = (
        "2026-05-07/2026-04-28T10:00:19.619113/Democracy_Club__07May2026 - 27-4-26.tsv"
    )
    elections = ["2026-05-07"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Enfield Highway Community Centre, 117 Hertford Road, Enfield
        if record.polling_place_id == "9815":
            record = record._replace(polling_place_easting="535189")
            record = record._replace(polling_place_northing="197091")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "207184074",  # MAINYARD STUDIOS, 58B ALEXANDRA ROAD, ENFIELD
                "207104137",  # BUSH HILL COTTAGE 20 BUSH HILL, SOUTHGATE
                "207037892",  # THE LODGE, SWEET BRIAR WALK, LONDON
                "207158629",  # NORTH LODGE, TRENT PARK, FERNY HILL, BARNET
                "207050654",  # S I G INTERIORS, UNIT 14A-14B, BANKSIA ROAD, LONDON
                "207026799",  # FLAT 1 51 BEATRICE ROAD, EDMONTON
                "207035572",  # 207A HERTFORD ROAD, ENFIELD
                "207142247",  # ENFIELD POUND PLUS STORE, 254-256 HERTFORD ROAD, ENFIELD
                "207030702",  # 293A HERTFORD ROAD, ENFIELD
                "207019443",  # FLAT 2 39A CHURCH STREET, EDMONTON
                "207019442",  # FLAT 1 39A CHURCH STREET, EDMONTON
                "207024608",  # FLAT 1, ELS COURT, 97 BULLSMOOR LANE, ENFIELD
                "207025235",  # 173B BOWES ROAD, SOUTHGATE
                "207136289",  # CONSERVATIVE CLUB 278 BAKER STREET, ENFIELD
                "207148523",  # 257 HERTFORD ROAD, ENFIELD
                "207024752",  # PHOTOVOLTAIC AND PREMISES CUCKOO HALL ACADEMY SCHOOL CUCKOO HALL LANE, EDMONTON
                "207025563",  # 81A NORTH CIRCULAR ROAD, LONDON
            ]
        ):
            return None

        if record.addressline6 in [
            # split
            "EN3 6HB",
            "EN2 9AQ",
            "EN2 9HQ",
            "N9 9QP",
            "EN2 0BZ",
            # suspect
            "N13 4HE",
            "EN1 1GL",
            "EN2 6NB",
            "EN3 6BP",
        ]:
            return None

        return super().address_record_to_dict(record)
