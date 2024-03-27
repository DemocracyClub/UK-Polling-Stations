from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RCH"
    addresses_name = (
        "2024-05-02/2024-03-27T10:00:00.966473/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-27T10:00:00.966473/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "23050342",  # 2 CHADWICK STREET, FIRGROVE, ROCHDALE
            "10023363964",  # 6 BELFIELD LANE, ROCHDALE
            "10094361530",  # APPLE VIEW 107 SHAW ROAD, ROCHDALE
            "10094361529",  # APPLE COTTAGE 105 SHAW ROAD, ROCHDALE
            "10094362473",  # 1 POPPY CLOSE, LITTLEBOROUGH
            "10094358281",  # 61H QUEEN VICTORIA STREET, ROCHDALE
            "10094358283",  # 61J QUEEN VICTORIA STREET, ROCHDALE
            "23040672",  # NADEN HOUSE, WOODHOUSE LANE, ROCHDALE
            "10096505235",  # HELLIWELL HOUSE, BUCKLEY HILL LANE, MILNROW, ROCHDALE
        ]:
            return None
        if record.addressline6.replace("\xa0", " ") in [
            # split
            "OL16 2SD",
            "OL10 1FH",
            "OL16 4XF",
            "M24 1LG",
            "OL10 4DG",
            "OL15 9LY",
            "OL15 0JH",
            "OL10 3BJ",
            "OL10 2JP",
            "OL16 1FD",
            "M24 2PR",
            "OL11 3AE",
            "OL10 3LW",
            "M24 6UE",
            "OL16 4RF",
            "M24 5BP",
            "OL12 0RE",
            # suspect
            "OL12 6GP",
            "OL12 9QA",
            "OL12 6GR",
            "OL12 0NU",
        ]:
            return None
        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Mobile Unit at The Black Dog Pub, On the corner of Redfearn Wood & Rooley Moor Road, Rochdale OL12 6JZ (2 polling stations)
        if record.polling_place_id in (
            "5442",
            "5515",
        ):
            record = record._replace(polling_place_postcode="OL12 7JG")
        return super().station_record_to_dict(record)
