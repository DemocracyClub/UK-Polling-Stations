from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "STF"
    addresses_name = (
        "2024-07-04/2024-06-03T11:06:55.323891/Democracy_Club__04July2024 (14).tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-03T11:06:55.323891/Democracy_Club__04July2024 (14).tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200003039580",  # ROACHSIDE, UPPER HULME, LEEK
            "10010605935",  # FAR BARN, QUARNFORD, BUXTON
            "200003038961",  # SHIRLEY & BOAM, WATERHOUSE FARM, LONGNOR, BUXTON
            "200003041029",  # INNKEEPERS COTTAGE, HULME END, BUXTON
            "200003038876",  # THE HILLOCKS BACK OF ECTON, ECTON
            "100031843397",  # BROOK HOUSE, SUGAR STREET, RUSHTON SPENCER, MACCLESFIELD
            "100031852897",  # HILL TOP COTTAGE, HOT LANE, BIDDULPH MOOR, STOKE-ON-TRENT
            "100031864940",  # 93 WOODHOUSE LANE, BIDDULPH, STOKE-ON-TRENT
            "100031857721",  # 29 PARK LANE, KNYPERSLEY, STOKE-ON-TRENT
            "100031861383",  # 1 SYTCH ROAD, BROWN EDGE, STOKE-ON-TRENT
            "200001048644",  # FIELDSVIEW FARM, ROWNALL ROAD, WETLEY ROCKS, STOKE-ON-TRENT
            "200001577505",  # 339A ASH BANK ROAD, WERRINGTON, STOKE-ON-TRENT
            "200001582118",  # HOMELEA, LEEK ROAD, WERRINGTON, STOKE-ON-TRENT
            "200001582743",  # GREENFIELD COTTAGE, WINNOTHDALE, TEAN, STOKE-ON-TRENT
            "200001582443",  # THE BARN HOUSE ILAM MOOR LANE, ILAM
            "200003038297",  # PLEASANT VIEW, UPPER HULME, LEEK
            "200003039868",  # IVY HOUSE FARM, ASHBOURNE ROAD, WHISTON, STOKE-ON-TRENT
        ]:
            return None

        if record.addressline6 in [
            # splits
            "ST13 8BS",
            "ST13 6BU",
            "ST8 7JW",
            "ST10 1LT",
            "ST9 9DQ",
            "ST10 1UB",
            "SK17 0QT",
            "ST13 5DP",
            "ST13 7QX",
            # suspect
            "ST10 2PR",
        ]:
            return None

        return super().address_record_to_dict(record)
