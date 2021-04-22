from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RIH"
    addresses_name = (
        "2021-04-09T11:16:17.947077/RichmondshireDemocracy_Club__06May2021.tsv"
    )
    stations_name = (
        "2021-04-09T11:16:17.947077/RichmondshireDemocracy_Club__06May2021.tsv"
    )
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10004781106",  # CALVERTS NOOK, THE GAITS, GAYLE, HAWES
            "10034642865",  # LOW CAMMS HOUSE, ASKRIGG, LEYBURN
            "10034645243",  # COVER BRIDGE BUNGALOW, EAST WITTON, LEYBURN
            "10034644048",  # ELLENGARTH, GARRISTON, LEYBURN
            "10090348320",  # OHLSON HOUSE BARDEN LANE, BARDEN
            "10012781811",  # NEW FARM HOUSE CRAGGS LANE FARM CRAGGS LANE, TUNSTALL
            "100051959949",  # GARDENERS COTTAGE RICHMOND ROAD, HIPSWELL
            "10034646179",  # STOTTERGILL GUNING LANE TO GUNNERSIDE, SATRON, GUNNERSIDE
            "10034641250",  # THEAS COTTAGE, SATRON, GUNNERSIDE, RICHMOND
            "10012784013",  # SATRON FARM, GUNNERSIDE, RICHMOND
            "10012784008",  # GILL HEAD, GUNNERSIDE, RICHMOND
            "10034642031",  # BENTS HOUSE, LOW ROW, RICHMOND
            "10034643612",  # THE BARN SPRING END FARM CRACKPOT TO GUNNERSIDE, LOW ROW
            "10034643695",  # BARNACRES BUNGALOW, SKEEBY, RICHMOND
            "10004782465",  # SKEEBY LODGE, SCURRAGH LANE, SKEEBY, RICHMOND
            "10034644313",  # GREENBERRY FARM, SOUTH COWTON, NORTHALLERTON
            "10004781639",  # THE OLD SMITHY, HALNABY GRANGE, NORTH COWTON, NORTHALLERTON
            "10034649653",  # CARAVAN AT STONEY STOOPS SCOTCH CORNER TO APPLEBY TRUNK ROAD, EAST LAYTON
            "10034645690",  # SAUNDERS HOUSE FARM SCOTCH CORNER TO APPLEBY TRUNK ROAD, EAST LAYTON
            "10034645324",  # RIVERBANK COTTAGE, ALDBROUGH ST. JOHN, RICHMOND
            "10012782380",  # BOBBIN MILL COTTAGE, GARRISTON, LEYBURN
            "10034644167",  # THE OLD BLACKSMITHS SHOP VILLAGE STREETS NORTH OF GREEN, REETH
            "10090348313",  # THE HAMMOND WAITLANDS LANE, RAVENSWORTH
        ]:
            return None

        if record.addressline6 in [
            "DL8 3EA",
            "DL8 4DH",
            "DL8 4AS",
            "DL8 4DY",
            "DL10 7ES",
            "DL9 4NN",
            "DL9 4RT",
            "DL9 4JA",
            "DL10 4SN",
            "DL9 3NJ",
            "DL10 7AZ",
            "DL9 4LA",
            "DL11 7TF",
            "DL11 7AE",
            "DL11 6RE",
            "DL11 6NT",
            "DL11 6JJ",
            "DL8 3DF",
            "DL8 3PN",
            "DL10 4TJ",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):

        if record.polling_place_id in [
            "6793",  # Aysgarth Village Hall, Main Street, Aysgarth DL8 3AH
            "6837",  # Colburn Village Hall, Colburn Lane, Colburn DL9 4LS
            "6848",  # North Cowton Village Hall, North Cowton, Northallerton DL7 0HR
            "6882",  # Hunton Village Hall, Ratten Row, Hunton DL8 1LY
            "6890",  # Harmby Village Hall, Hillfoot, Harmby DL8 5PG
            "6900",  # Newton-le-Willows Village Hall, Newton-le-Willows DL8 1SB
            "6931",  # Middleton Tyas Memorial Hall, The Green, Middleton Tyas, Richmond, North Yorkshire DL10 6PP
            "6935",  # Skeeby Village Hall, Richmond Road, Skeeby DL10 5DX
            "6939",  # Eppleby Village Hall, Chapel Row, Eppleby DL11 7AP
            "6978",  # Richmond Market Hall, Market Place, Richmond DL10 4JJ
            "7002",  # Muker Public Hall, Muker DL11 6QG
        ]:
            record = record._replace(polling_place_postcode="")

        return super().station_record_to_dict(record)
