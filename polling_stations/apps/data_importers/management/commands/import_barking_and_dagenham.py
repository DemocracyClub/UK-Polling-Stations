from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BDG"
    addresses_name = (
        "2022-05-05/2022-04-11T14:50:24.315074/Democracy_Club__05May2022.CSV"
    )
    stations_name = (
        "2022-05-05/2022-04-11T14:50:24.315074/Democracy_Club__05May2022.CSV"
    )
    elections = ["2022-05-05"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10091590964",  # 563 WOOD LANE, DAGENHAM
            "10091590961",  # 557 WOOD LANE, DAGENHAM
            "10091590971",  # 577 WOOD LANE, DAGENHAM
            "10091590976",  # 587 WOOD LANE, DAGENHAM
            "10091590978",  # 591 WOOD LANE, DAGENHAM
            "10091590974",  # 583 WOOD LANE, DAGENHAM
        ]:
            return None

        if record.addressline6 in [
            "RM8 1DF",
            "IG11 7XS",
            "IG11 9BW",
            "RM10 7TD",
            "IG11 9EA",
            "RM6 6DJ",
            "RM9 4DS",
            "RM9 4QR",
            "RM10 8BX",
        ]:
            return None

        return super().address_record_to_dict(record)
