from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CHI"
    addresses_name = (
        "2026-05-07/2026-03-03T14:03:00.501439/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-03-03T14:03:00.501439/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                "10002483304",  # RIVER BARN, SELHAM, PETWORTH, GU28 0PS
                "10093118500",  # MARTINS FARMHOUSE, CONNOLLY WAY, CHICHESTER, PO19 6WD
                "10002482962",  # SWAN HOUSE, BURTON PARK ROAD, PETWORTH, GU28 0JU
                "10008884917",  # PUMP HOUSE, BEECHWOOD LANE, LAVINGTON PARK, PETWORTH, GU28 0NA
                "10002470140",  # THE STABLE HOUSE, FYNING HILL, ROGATE, PETERSFIELD, GU31 5BU
                "100062411430",  # CONNOLLY HOUSE, CONNOLLY WAY, CHICHESTER
                "10090340673",  # FLAT, CO-OPERATIVE RETAIL SERVICES LTD, OLIVER WHITBY ROAD, CHICHESTER
                "10008884574",  # PADDOCK HOUSE, PLAISTOW ROAD, LOXWOOD, BILLINGSHURST
                "10002469404",  # NEWLANDS COTTAGE, LINCHMERE, HASLEMERE
                "10008887597",  # THE GRANARY UPWALTHAM HOUSE FARM CHURCH FARM LANE, UPWALTHAM
                "200001740959",  # BADGERS, BORDER CLOSE, HILL BROW, LISS
                "10002467828",  # PALFREY FARM, LONDON ROAD, PETWORTH
                "10014107960",  # HORSESHOE HOUSE, HENLEY HILL, HENLEY, HASLEMERE
                "100061753348",  # GIG HOUSE, STUBCROFT LANE, EAST WITTERING, CHICHESTER
            ]
        ):
            return None

        if record.addressline6 in [
            # split
            "PO18 8QG",
            "PO18 0PR",
            "PO19 3PX",
            "GU29 9QT",
            "RH20 1PW",
            "PO10 8PR",
            "PO20 9AD",
            "GU28 9LY",
            "PO19 7QL",
            #  suspect
            "PO20 8NX",
            "PO20 8SP",
            "RH14 0JF",
            "RH14 0JY",
            "PO19 6AA",
            "PO20 9BL",
            "PO18 9JG",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # WARNING: Polling station Rake Village Hall (6221) is in East Hampshire District Council (EHA)
        # Correct address, it is on the border of the two councils

        # Postcode correction for: Selsey Community Leisure Centre, Manor Road, Selsey, Chichester, West Sussex, PO20 2SE
        if record.polling_place_id == "6228":
            record = record._replace(polling_place_postcode="PO20 0SE")

        return super().station_record_to_dict(record)
