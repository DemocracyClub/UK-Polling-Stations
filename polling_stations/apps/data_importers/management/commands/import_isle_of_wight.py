from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "IOW"
    addresses_name = (
        "2026-05-07/2026-04-07T16:00:02.432211/Democracy_Club__07May2026_fixed.CSV"
    )
    stations_name = (
        "2026-05-07/2026-04-07T16:00:02.432211/Democracy_Club__07May2026_fixed.CSV"
    )
    elections = ["2026-05-07"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100060763282",  # 28A HIGH STREET, RYDE
            "10023714741",  # FYNELEA, PRINCES ROAD, FRESHWATER
            "200001868290",  # THE ORCHARDS, PRINCES ROAD, FRESHWATER
            "100062441673",  # WHITE COTTAGE, MILITARY ROAD, ATHERFIELD, VENTNOR
            "10024249197",  # BATTS LODGE, BATTS ROAD, SHANKLIN
            "10003318523",  # THE FIELD, MAIN ROAD, HAVENSTREET, RYDE
        ]:
            return None

        if record.addressline6 in [
            # split
            "PO30 2DH",
            "PO36 9NQ",
        ]:
            return None

        return super().address_record_to_dict(record)
