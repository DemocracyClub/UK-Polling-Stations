from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RCH"
    addresses_name = (
        "2024-02-29/2024-02-12T10:11:09.302381/Democracy_Club__29February2024 1.tsv"
    )
    stations_name = (
        "2024-02-29/2024-02-12T10:11:09.302381/Democracy_Club__29February2024 1.tsv"
    )
    elections = ["2024-02-29"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "23050342",  # 2 CHADWICK STREET, FIRGROVE, ROCHDALE
            "10023363964",  # 6 BELFIELD LANE, ROCHDALE
            "10094361530",  # APPLE VIEW 107 SHAW ROAD, ROCHDALE
            "10094361529",  # APPLE COTTAGE 105 SHAW ROAD, ROCHDALE
            "23099722",  # 12B MANCHESTER ROAD, HEYWOOD
            "10094362473",  # 1 POPPY CLOSE, LITTLEBOROUGH
        ]:
            return None

        if record.addressline6.replace("\xa0", " ") in [
            # split
            "CV10 9QF",
            "OL16 1FD",
            "OL15 9LY",
            "OL15 0JH",
            "OL16 2SD",
            "OL16 4XF",
            "OL16 4RF",
            # suspicious
            "OL12 6GP",
            "OL12 9QA",
            "OL12 6GR",
            "OL12 0NU",
            "OL11 2HF",
        ]:
            return None

        return super().address_record_to_dict(record)
