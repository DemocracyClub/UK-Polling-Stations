from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HAV"
    addresses_name = (
        "2024-05-02/2024-02-22T13:39:51.268605/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-02-22T13:39:51.268605/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10033421759",  # GROVE FARM, BROOK STREET, BRENTWOOD
            "10033422184",  # 57 NAGS HEAD LANE, BRENTWOOD
            "10033425629",  # THE FARM HOUSE BROADFIELDS FARM PIKE LANE, UPMINSTER
            "100021384326",  # 97 LOWER BEDFORDS ROAD, ROMFORD
            "10033422378",  # 17 KILN WOOD LANE, HAVERING-ATTE-BOWER, ROMFORD
            "100021370259",  # 98 DEE WAY, ROMFORD
            "10091580271",  # FLAT 1 171 NORTH STREET, ROMFORD
            "100023219217",  # 175A OLDCHURCH ROAD, ROMFORD
            "100021390436",  # 3-5 PARK END ROAD, ROMFORD
            "100021326271",  # 43 CLYDESDALE ROAD, HORNCHURCH
            "100021326269",  # 41 CLYDESDALE ROAD, HORNCHURCH
            "200002675962",  # THE WINDMILL, 167 UPMINSTER ROAD, UPMINSTER
            "200002668849",  # UPPER BEDFORDS FARM, LOWER BEDFORDS ROAD, ROMFORD
            "100021384325",  # 83 LOWER BEDFORDS ROAD, ROMFORD
            "100021322397",  # 2A ARDLEIGH GREEN ROAD, HORNCHURCH
        ]:
            return None

        if record.addressline6 in [
            # splits
            "RM11 2BY",
            "RM12 4LG",
            "RM7 8DX",
            "RM7 7BX",
            # looks wrong
            "RM12 6SH",
        ]:
            return None

        return super().address_record_to_dict(record)
