from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "STF"
    addresses_name = (
        "2024-05-02/2024-04-10T15:59:38.268252/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-04-10T15:59:38.268252/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
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
            "ST9 9DQ",
            "ST13 5DP",
            "ST13 8BS",
            "ST13 7QX",
            "ST10 1LT",
            "ST13 6BU",
            "ST8 7JW",
            "SK17 0QT",
            "ST10 1UB",
            "ST10 2PR",  # RICHMOOR HILL, DILHORNE, STOKE-ON-TRENT
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Quarnford Village Hall, Flash, Buxton, SK17 OSW
        # Postcode mistype, should be a number "0" instead of letter "O"
        # Easting and northing correction as location on the map is still quite off
        if record.polling_place_id == "8873":
            record = record._replace(
                polling_place_postcode="SK17 0SW",
                polling_place_easting="402802",
                polling_place_northing="367332",
            )
        # Hollinsclough Chapel Hall Hollinsclough, Longnor, Nr Buxton, SK17 ORH
        # Postcode mistype, should be a number "0" instead of letter "O"
        # Easting and northing correction as location on the map is still quite off
        if record.polling_place_id == "8774":
            record = record._replace(
                polling_place_postcode="SK17 0RH",
                polling_place_easting="406497",
                polling_place_northing="366542",
            )

        # St. Bartholomew`s School, Buxton Road, Longnor, Buxton, SK17 ONZ
        # Postcode mistype, should be a number "0" instead of letter "O"
        if record.polling_place_id == "8764":
            record = record._replace(
                polling_place_postcode="SK17 0NZ",
            )

        # Sheen Village Hall, Sheen, Buxton, SK17 OES
        # Postcode mistype, should be a number "0" instead of letter "O"
        # Easting and northing correction as location on the map is still quite off
        if record.polling_place_id == "8905":
            record = record._replace(
                polling_place_postcode="SK17 0ES",
                polling_place_easting="411301",
                polling_place_northing="361466",
            )

        # Werrington Village Hall, Ash Bank Road, Werrington, Stoke-on-Trent, ST9 1JS
        # Easting and northing correction as location on the map is still quite off
        if record.polling_place_id == "8778":
            record = record._replace(
                polling_place_postcode="ST9 0JS",
                polling_place_easting="393754",
                polling_place_northing="347218",
            )

        # Warslow Village Hall, Cheadle Road, Warslow, Near Buxton, Derbyshire, SK17 OJJ
        # Postcode mistype, should be a number "0" instead of letter "O"
        # Easting and northing correction as location on the map is still quite off
        if record.polling_place_id == "8924":
            record = record._replace(
                polling_place_postcode="SK17 0JJ",
                polling_place_easting="408601",
                polling_place_northing="358540",
            )

        # The following are suspect postcodes:

        # Foxt Village Hall, Foxt Road, Foxt, Stoke on Trent ST10 2HY
        if record.polling_place_id == "8901":
            record = record._replace(
                polling_place_postcode="",
            )

        # Cauldon Lowe Village Hall, Cauldon Lowe, Nr Waterhouses, Stoke on Trent ST10 3HW
        if record.polling_place_id == "8858":
            record = record._replace(
                polling_place_postcode="",
            )
        return super().station_record_to_dict(record)
