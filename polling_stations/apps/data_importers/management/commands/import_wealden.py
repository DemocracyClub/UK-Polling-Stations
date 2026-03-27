from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WEA"
    addresses_name = (
        "2026-05-07/2026-03-27T16:12:54.336801/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-27T16:12:54.336801/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    # Below warnings checked and no correction required:
    # WARNING: Polling station Ashurst Wood Village Centre (9329) is in Mid Sussex District Council (MSS)

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10033415978",  # BLACKBERRY FARM, BUTCHERFIELD LANE, HARTFIELD
            "10091054596",  # TWOAKS, ERIDGE ROAD, CROWBOROUGH
            "10070937881",  # 2 WINSCOMBE GARDENS, BEACON ROAD, CROWBOROUGH
            "10070937880",  # 1 WINSCOMBE GARDENS, BEACON ROAD, CROWBOROUGH
            "10033411585",  # WATER MILL FARM, BODLE STREET GREEN, HAILSHAM
            "10033409987",  # RICKNEY FARM, RICKNEY, HAILSHAM
            "10033401022",  # THE OLD GRANARY, BERWICK, POLEGATE
            "10033400614",  # FIR TREE COTTAGE, HEATHFIELD ROAD, HALLAND, LEWES
        ]:
            return None

        if record.addressline6 in [
            # looks wrong
            "BN8 6BA",
        ]:
            return None

        return super().address_record_to_dict(record)
