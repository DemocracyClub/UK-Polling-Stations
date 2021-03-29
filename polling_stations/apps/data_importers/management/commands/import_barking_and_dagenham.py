from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BDG"
    addresses_name = "2021-03-26T10:53:59.286963/Barking Democracy_Club__06May2021.CSV"
    stations_name = "2021-03-26T10:53:59.286963/Barking Democracy_Club__06May2021.CSV"
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100101100",  # SACRED HEART CONVENT 191 GORESBROOK ROAD, DAGENHAM
            "10091590964",  # 563 WOOD LANE, DAGENHAM
            "100067244",  # 7 TRINIDAD GARDENS, DAGENHAM
            "100092451",  # TOBY CARVERY, WHALEBONE LANE NORTH, ROMFORD
            "10091590961",  # 557 WOOD LANE, DAGENHAM
            "10091590971",  # 577 WOOD LANE, DAGENHAM
            "100072494",  # 3 ROSE HATCH AVENUE, ROMFORD
            "10091590976",  # 587 WOOD LANE, DAGENHAM
            "10091590978",  # 591 WOOD LANE, DAGENHAM
            "10091590974",  # 583 WOOD LANE, DAGENHAM
            "10023598803",  # 135A SALISBURY AVENUE, BARKING
            "100012133",  # 939A GREEN LANE, DAGENHAM
            "100100597",  # MANOR SCHOOL HOUSE SCHOOL SITE SANDRINGHAM ROAD, BARKING
            "10094447521",  # ANNEX TO 7 7A TRINIDAD GARDENS, DAGENHAM
        ]:
            return None

        if record.addressline6 in [
            "IG11 9BW",
            "RM8 3UH",
            "RM10 7TD",
            "RM8 2GT",
            "RM8 1BX",
            "RM9 4QR",
            "RM9 6XH",
            "RM9 5EA",
            "IG11 8FE",
            "RM8 3PT",
            "RM6 5QX",
            "RM8 1BJ",
            "RM9 6XG",
            "IG11 9NW",
            "IG11 9EA",
            "RM10 7UU",
            "RM10 8DT",
            "RM10 8BX",
            "RM8 3UB",
            "RM6 5RA",
            "RM9 4DS",
            "IG11 8RF",
            "RM6 6RB",
            "RM9 6FG",
        ]:
            return None

        return super().address_record_to_dict(record)
