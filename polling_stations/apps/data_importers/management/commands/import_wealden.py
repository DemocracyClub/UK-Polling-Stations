from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WEA"
    addresses_name = (
        "2024-07-04/2024-06-04T15:05:04.859578/Democracy_Club__04July2024 Xpress.tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-04T15:05:04.859578/Democracy_Club__04July2024 Xpress.tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10033415978",  # BLACKBERRY FARM, BUTCHERFIELD LANE, HARTFIELD
            "10091054596",  # TWOAKS, ERIDGE ROAD, CROWBOROUGH
            "10070937881",  # 2 WINSCOMBE GARDENS, BEACON ROAD, CROWBOROUGH
            "10070937880",  # 1 WINSCOMBE GARDENS, BEACON ROAD, CROWBOROUGH
            "10091055379",  # THE LITTLE BARN, BAKERY LANE, PUNNETTS TOWN, HEATHFIELD
            "10033411585",  # WATER MILL FARM, BODLE STREET GREEN, HAILSHAM
            "10033409987",  # RICKNEY FARM, RICKNEY, HAILSHAM
            "10033401022",  # THE OLD GRANARY, BERWICK, POLEGATE
            "10033416937",  # BLUEBELL VIEW, WHITESMITH, LEWES
            "10024378003",  # HOLLOW LANE VINEYARD, HOLLOW LANE, BLACKBOYS, UCKFIELD
            "10091054700",  # MOBILE HOME HOLLOW LANE VINEYARD HOLLOW LANE, BLACKBOYS
            "10033400614",  # FIR TREE COTTAGE, HEATHFIELD ROAD, HALLAND, LEWES
            "10096307522",  # CARAVAN FIR TREE COTTAGE HEATHFIELD ROAD, HALLAND
            "100060135936",  # CORNER COTTAGE, BROWNS LANE, UCKFIELD
            "100060131130",  # WINDLEBROOK, BAYLEYS LANE, WILMINGTON, POLEGATE
        ]:
            return None

        if record.addressline6 in [
            # splits
            "BN27 4UX",
            "TN22 5TR",
            # looks wrong
            "BN8 6BA",
            "BN27 1DQ",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Below warnings checked and no correction required:
        # WARNING: Polling station Ashurst Wood Village Centre (9329) is in Mid Sussex District Council (MSS)

        # postcode correction for: Rose Room, Forest Row Community Centre, Hartfield Road, Forest Row, RH18
        if record.polling_place_id == "9728":
            record = record._replace(polling_place_postcode="RH18 5DZ")

        return super().station_record_to_dict(record)
