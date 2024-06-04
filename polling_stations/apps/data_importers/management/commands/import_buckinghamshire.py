from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "BUC"
    addresses_name = "2024-07-04/2024-06-10T14:53:02.994870/buc-combined.tsv"
    stations_name = "2024-07-04/2024-06-10T14:53:02.994870/buc-combined.tsv"
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "766271522",  # CLOVERHILL HOUSE IVY LANE, GREAT BRICKHILL
            "766297815",  # MANOR FARM, HILLESDEN ROAD, GAWCOTT, BUCKINGHAM HOUSE IVY LANE, GREAT BRICKHILL
            "10092750629",  # HQ AIR COMMAND HURRICANE BUILDING RAF HIGH WYCOMBE NEW ROAD, WALTERS ASH
            "10033201817",  # STABLE COTTAGE, HARLEYFORD LANE, MARLOW
            "200000812734",  # TEMPLE LOCK HOUSE HARLEYFORD LANE, MARLOW
            "10013781402",  # MOBILE HOME ST GEORGES HALL WHITE LION ROAD, LITTLE CHALFONT
        ]:
            return None

        if record.addressline6 in [
            # split
            "HP21 9HY",
            "HP8 4QT",
            "SL9 9FH",
            "HP23 6NG",
            "MK18 1PJ",
            "SL9 9JH",
            "RG9 6JH",
            # suspect
            "HP12 3HP",  # MCLELLAN PLACE
            "SL3 6QH",  # CROMWELLS COURT
        ]:
            return None

        return super().address_record_to_dict(record)
