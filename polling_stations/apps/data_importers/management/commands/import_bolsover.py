from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BOS"
    addresses_name = (
        "2025-05-01/2025-02-26T09:47:14.141094/Democracy_Club__01May2025.tsv"
    )
    stations_name = (
        "2025-05-01/2025-02-26T09:47:14.141094/Democracy_Club__01May2025.tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100030071192",  # SOUTHFIELD LODGE, BAKESTONE MOOR, WHITWELL, WORKSOP
            "200004511872",  # 31 OXCROFT LANE, OXCROFT, CHESTERFIELD
            "100032019011",  # SCHOOL HOUSE, CHURCH HILL, BLACKWELL, ALFRETON
            "10013073817",  # 31B CHURCH STREET, SOUTH NORMANTON
            "200002768236",  # GRANGE FARM, BIRCHWOOD LANE, SOUTH NORMANTON, ALFRETON
            "10013068442",  # CHERRY TREE BARN, SPRING LANE, ELMTON, WORKSOP
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Mobile Unit, Whaley Common Adjacent Henton Memorial Hall, Whaley Common, Langwith, Mansfield
        if record.polling_place_id == "6400":
            record = record._replace(polling_place_postcode="NG20 9HU")

        # Whaley Thorns and Langwith Village Hall, Portland Road, Langwith, Mansfield, NG20 9EZ
        if record.polling_place_id == "6295":
            record = record._replace(
                polling_place_easting="453287",
                polling_place_northing="371077",
            )

        # Bolsover Parish Rooms, Hornscroft Road, Bolsover, Chesterfield, S44 6HG
        if record.polling_place_id == "6392":
            record = record._replace(
                polling_place_easting="447491",
                polling_place_northing="370263",
            )

        return super().station_record_to_dict(record)
