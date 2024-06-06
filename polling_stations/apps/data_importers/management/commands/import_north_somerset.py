from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NSM"
    addresses_name = (
        "2024-07-04/2024-06-06T09:25:50.552110/Democracy_Club__04July2024.CSV"
    )
    stations_name = (
        "2024-07-04/2024-06-06T09:25:50.552110/Democracy_Club__04July2024.CSV"
    )
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "24138946",  # FLAT AT STAR INN RHODYATE HILL, BRISTOL
            "24080907",  # MARLBRO, THE BATCH, BACKWELL, BRISTOL
            "24155623",  # 71 LYEFIELD ROAD, KEWSTOKE, WESTON-SUPER-MARE
            "24014702",  # 30A BYRON ROAD, LOCKING, WESTON-SUPER-MARE
            "24141074",  # 11A BYRON ROAD, WESTON-SUPER-MARE
            "24013232",  # 6 PURN LANE, WESTON-SUPER-MARE
            "24076278",  # ASHTON HILL HOUSE, WESTON ROAD, FAILAND, BRISTOL
        ]:
            return None

        if record.addressline6 in [
            # splits
            "BS24 8GE",
            "BS20 0LJ",
            "BS22 6EA",
            # suspect
            "BS23 1WN",
            "BS23 1FH",
        ]:
            return None

        return super().address_record_to_dict(record)
