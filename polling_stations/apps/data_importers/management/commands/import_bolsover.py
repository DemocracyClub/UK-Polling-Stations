from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BOS"
    addresses_name = (
        "2023-05-04/2023-04-11T13:09:30.661328/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-04-11T13:09:30.661328/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200004520294",  # THE HERMITAGE, WALLS LANE, BARLBOROUGH, CHESTERFIELD
            "10013072329",  # 1 BOWDEN COURT, CLOWNE
            "100030071192",  # SOUTHFIELD LODGE, BAKESTONE MOOR, WHITWELL, WORKSOP
            "200004511872",  # 31 OXCROFT LANE, OXCROFT, CHESTERFIELD
            "10034144937",  # NEWTON WOOD FARM, NEWTON, ALFRETON
            "100032019011",  # SCHOOL HOUSE, CHURCH HILL, BLACKWELL, ALFRETON
            "10013073817",  # 31B CHURCH STREET, SOUTH NORMANTON
            "200002768236",  # GRANGE FARM, BIRCHWOOD LANE, SOUTH NORMANTON, ALFRETON
            "200004511974",  # 32 OXCROFT LANE, OXCROFT, CHESTERFIELD
            "200004511975",  # 33 OXCROFT LANE, OXCROFT, CHESTERFIELD
            "200004520437",  # DAMSBROOK FARM COTTAGE, OXCROFT ESTATE, MANSFIELD ROAD, OXCROFT, WORKSOP
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Mobile Unit, Whaley Common Adjacent Henton Memorial Hall, Whaley Common, Langwith, Mansfield
        if record.polling_place_id == "4879":
            record = record._replace(polling_place_postcode="NG20 9HU")

        # Whaley Thorns and Langwith Village Hall, Portland Road, Langwith, Mansfield, NG20 9EZ
        if record.polling_place_id == "4907":
            record = record._replace(
                polling_place_easting="453287",
                polling_place_northing="371077",
            )

        # Bolsover Parish Rooms, Hornscroft Road, Bolsover, Chesterfield, S44 6HG
        if record.polling_place_id == "4876":
            record = record._replace(
                polling_place_easting="447491",
                polling_place_northing="370263",
            )

        return super().station_record_to_dict(record)
