from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SLF"
    addresses_name = (
        "2026-05-07/2026-03-17T10:59:10.971611/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-17T10:59:10.971611/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10004682203",  # ALDERWOOD COTTAGE, LEIGH ROAD, WORSLEY, MANCHESTER
            "10095311109",  # APARTMENT 1, THORNCLIFFE, 48 VINE STREET, SALFORD
            "100012471364",  # WESTWOOD LODGE, PARRIN LANE, ECCLES, MANCHESTER
            "100011357863",  # 2A DUDLEY ROAD, CADISHEAD, MANCHESTER
            "100011424265",  # 47 VINE STREET, SALFORD
            "10095868168",  # 569 LIVERPOOL STREET, SALFORD
            "10095868167",  # 567 LIVERPOOL STREET, SALFORD
            "10095868166",  # 565 LIVERPOOL STREET, SALFORD
            "100012698449",  # ECCLES COLLEGE, CHATSWORTH ROAD, ECCLES, MANCHESTER
            "10095311112",  # APARTMENT 4, THORNCLIFFE, 48 VINE STREET, SALFORD
            "10095311110",  # APARTMENT 2, THORNCLIFFE, 48 VINE STREET, SALFORD
            "10095311111",  # APARTMENT 3, THORNCLIFFE, 48 VINE STREET, SALFORD
            "10095311117",  # APARTMENT 9, THORNCLIFFE, 48 VINE STREET, SALFORD
            "10095311120",  # APARTMENT 12, THORNCLIFFE, 48 VINE STREET, SALFORD
        ]:
            return None

        if record.addressline6 in [
            # splits
            "M27 0JE",
            # looks wrong
            "M27 4BL",
            "M6 8EZ",
            "M30 9RT",
            "M30 9ED",
        ]:
            return None

        return super().address_record_to_dict(record)
