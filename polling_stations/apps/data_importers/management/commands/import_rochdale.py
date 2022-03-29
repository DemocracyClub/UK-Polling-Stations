from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RCH"
    addresses_name = (
        "2022-05-05/2022-03-29T14:33:18.331708/Democracy_Club1__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-29T14:33:18.331708/Democracy_Club1__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Bangladesh Association And Community Project, 108 Ramsay Street, Rochdale
        if record.polling_place_id == "4456":
            # source: https://www.ourrochdale.org.uk/kb5/rochdale/directory/service.page?id=I9fU13_4zqc
            record = record._replace(polling_place_postcode="OL16 2EZ")  # was 'OL16 2E'

        # Falinge Park Bowling Club, Falinge Park, Heights Lane, Rochdale
        if record.polling_place_id == "4253":
            # 700m too far South; might be the wrong postcode
            record = record._replace(polling_place_postcode="")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "23050342",  # 2 CHADWICK STREET, FIRGROVE, ROCHDALE
            "10023363964",  # 6 BELFIELD LANE, ROCHDALE
            "23040672",  # NADEN HOUSE, WOODHOUSE LANE, ROCHDALE
            "23099722",  # 12B MANCHESTER ROAD, HEYWOOD
        ]:
            return None

        if record.addressline6 in [
            "OL11 3AE",
            "OL16 2SD",
            "M24 4FJ",
            "OL15 0JH",
            "OL11 5TR",
            "M24 2PR",
            "OL15 9LY",
            "OL10 2JP",
            "M24 1LG",
            "OL10 3BJ",
            "OL16 1FD",
            "OL10 1FH",
            "OL10 3LW",
            "OL16 4XF",
            "M24 6DW",
            "OL10 4DG",
            "M24 6UE",
            "OL16 4RF",
        ]:
            return None  # split

        return super().address_record_to_dict(record)
