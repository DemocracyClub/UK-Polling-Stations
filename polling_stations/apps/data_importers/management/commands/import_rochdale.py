from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RCH"
    addresses_name = (
        "2024-07-04/2024-06-05T12:19:57.871196/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-05T12:19:57.871196/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    # Checked and no correction needed
    # WARNING: Polling station Room At Rear of St James Church (6165) is in Oldham Metropolitan Borough Council (OLD)

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
            "23108010",  # HIGHER ASHWORTH FARM, MEADOW HEAD LANE, ROCHDALE
            "23026616",  # 1220 EDENFIELD ROAD, ROCHDALE
            "23040679",  # BROWN HILL FARM, WOODHOUSE LANE, ROCHDALE
        ]:
            return None
        if record.addressline6.replace("\xa0", " ") in [
            # split
            "OL12 0RE",
            "OL10 1FH",
            "OL16 2SD",
            "OL10 4DG",
            "OL10 3BJ",
            "OL11 3AE",
            "M24 2PR",
            "OL16 4XF",
            "M24 1LG",
            "OL10 3LW",
            "OL15 0JH",
            "OL15 9LY",
            "OL10 2JP",
            "M24 6UE",
            "OL16 1FD",
            "OL16 4RF",
            "M24 5BP",
            # suspect
            "OL12 6GP",
            "OL12 9QA",
            "OL12 6GR",
            "OL12 0NU",
            "OL10 1FU",
        ]:
            return None
        return super().address_record_to_dict(record)
