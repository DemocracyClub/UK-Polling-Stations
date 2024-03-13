from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "EHA"
    addresses_name = (
        "2024-05-02/2024-03-13T17:38:37.672177/Democracy_Club__02May2024 (1).tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-13T17:38:37.672177/Democracy_Club__02May2024 (1).tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "1710037869",  # BRIDGE MILL, MILL LANE, PETERSFIELD
            "10094122558",  # THE LITTLE BARN, WOODSIDE FARM, GOSPORT ROAD, PRIVETT, ALTON
            "10032905833",  # ANNEXE THE HOPKILN FRITH END ROAD, FRITH END, BORDON
            "10094123612",  # WATERCRESS COTTAGE, STATION ROAD, BENTLEY, FARNHAM
            "10094121538",  # THE STABLES, COLDREY FARM, LOWER FROYLE, ALTON
            "10009812215",  # THE LITTLE BARN, WOODSIDE FARM, GOSPORT ROAD, PRIVETT, ALTON
            "10094121982",  # TREESIDE VIEW, THE SHRAVE, FOUR MARKS, ALTON
            "10094122454",  # LUMBRY BARN, SELBORNE ROAD, ALTON
            "10094123735",  # OAK LODGE, SELBORNE ROAD, ALTON
            "1710105096",  # 21 WINCHESTER ROAD, ALTON
            "10032905135",  # HALF ACRE, HAWKLEY ROAD, LISS
            "10009812211",  # THE COTTAGE, LOWER BORDEAN, BORDEAN, PETERSFIELD
            "10096347180",  # RHODESIDE THE SHRAVE, FOUR MARKS, ALTON
            "100060259943",  # KITWOOD PLACE, SWELLING HILL, ROPLEY, ALRESFORD
            "10032907288",  # KITCOMBE BARN, KITCOMBE LANE, FARRINGDON, ALTON
            "1710109658",  # THE HERMITAGE, HEADLEY HILL ROAD, HEADLEY, BORDON
        ]:
            return None

        if record.addressline6 in [
            # splits
            "GU33 7BB",
            "GU30 7QL",
            "PO8 0QR",
        ]:
            return None

        return super().address_record_to_dict(record)
