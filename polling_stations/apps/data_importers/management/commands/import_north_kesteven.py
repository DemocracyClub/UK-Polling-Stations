from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NKE"
    addresses_name = (
        "2023-05-04/2023-03-28T22:10:40.359076/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-28T22:10:40.359076/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10006510463",  # SLATE HOUSE FARM, MIDDLE FEN LANE, WASHINGBOROUGH, LINCOLN
            "10006545127",  # OXFORD HOUSE, SLEAFORD ROAD, NOCTON HEATH, LINCOLN
            "10006503842",  # THE BUNGALOW, MARTIN MOOR, METHERINGHAM, LINCOLN
            "10006529962",  # THE BUNGALOW CAMPANET TATTERSHALL ROAD, BILLINGHAY, LINCOLN
            "10006507711",  # FLAT SLEAFORD GOLF CLUB WILLOUGHBY ROAD, GREYLEES, SLEAFORD
            "10006534879",  # CARAVAN AT MANOR COTTAGE SKINNAND PARSONS LANE, NAVENBY, LINCOLN
            "100030854102",  # MILL HOUSE, ROSE COTTAGE LANE, COLEBY, LINCOLN
        ]:
            return None

        if record.addressline6 in [
            "LN4 1EP",
            "LN4 2FA",
            "NG34 8AA",
        ]:
            return None

        return super().address_record_to_dict(record)
