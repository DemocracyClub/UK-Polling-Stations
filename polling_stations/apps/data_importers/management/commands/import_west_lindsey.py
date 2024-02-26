from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WLI"
    addresses_name = (
        "2024-05-02/2024-02-26T10:56:28.928696/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-02-26T10:56:28.928696/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10034686366",  # THE COTTAGE, LAUGHTON WOOD CORNER, LAUGHTON, GAINSBOROUGH
            "10034686362",  # PINE VIEW COTTAGE, LAUGHTON WOOD CORNER, LAUGHTON, GAINSBOROUGH
            "100032029197",  # EAST LODGE, THE BELT ROAD, GAINSBOROUGH
            "10034697585",  # THORNOCK GROVE FARM COTTAGE, THE BELT ROAD, GAINSBOROUGH
            "100032029197",  # EAST LODGE, THE BELT ROAD, GAINSBOROUGH
            "10013815969",  # WEST VIEW FARM, STOW PARK, LINCOLN
            "10090696854",  # HORIZON BARN, BULLY HILL TOP, TEALBY, MARKET RASEN
            "200001151020",  # HILL CREST, BULLY HILL TOP, TEALBY, MARKET RASEN
            "10013810973",  # WOLD VIEW HOUSE, BULLY HILL TOP, TEALBY, MARKET RASEN
            "10013809476",  # SWINTHORPE HOUSE, SNARFORD, MARKET RASEN
            "100030954683",  # WEST WHARTON FARM, MILL LANE, MORTON, GAINSBOROUGH
            "10013809617",  # GREENFIELD HOUSE, LISSINGLEY LANE, LISSINGTON, LINCOLN
            "10013809613",  # LISSINGLEA HOUSE FARM, LISSINGLEY LANE, LISSINGTON, LINCOLN
            "10013812180",  # 1 NETTLETON PARK MOORTOWN ROAD, NETTLETON, MARKET RASEN
        ]:
            return None

        if record.addressline6 in [
            ## split
            "DN21 1HL",
            "DN21 1TU",
            "LN8 3SU",
            "LN2 3PD",
            # suspect
            "LN8 6JA",
            "LN8 5SF",
        ]:
            return None

        return super().address_record_to_dict(record)
