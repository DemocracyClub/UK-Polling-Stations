from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RCH"
    addresses_name = (
        "2023-05-04/2023-03-09T13:27:25.433057/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-09T13:27:25.433057/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Polling station Room At Rear of St James Church -> Checked & OK

        if record.polling_place_id in [
            "4660",  # Mobile Unit at The Black Dog Pub
            "4728",  # Mobile Unit at The Black Dog Pub
            "4585",  # Falinge Park Bowling Club
        ]:
            record = record._replace(polling_place_postcode="")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "23050342",  # 2 CHADWICK STREET, FIRGROVE, ROCHDALE
            "10023363964",  # 6 BELFIELD LANE, ROCHDALE
            "23040672",  # NADEN HOUSE, WOODHOUSE LANE, ROCHDALE
            "10094362349",  # 10 FRANCIS CLOSE, MIDDLETON, MANCHESTER
        ]:
            return None

        if record.addressline6 in [
            "OL10 1FH",
            "OL10 3BJ",
            "OL15 9LY",
            "OL15 0JH",
            "OL11 3AE",
            "M24 4FJ",
            "M24 2PR",
            "OL16 4XF",
            "OL16 2SD",
            "OL10 4DG",
            "OL16 4RF",
            "M24 6UE",
            "M24 6DW",
            "OL16 1FD",
            "OL10 2JP",
            "M24 1LG",
            "OL10 3LW",
        ]:
            return None  # split

        return super().address_record_to_dict(record)
