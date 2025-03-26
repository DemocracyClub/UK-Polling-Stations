from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CHI"
    addresses_name = (
        "2025-05-01/2025-03-26T14:28:46.054551/Democracy_Club__01May2025.CSV"
    )
    stations_name = (
        "2025-05-01/2025-03-26T14:28:46.054551/Democracy_Club__01May2025.CSV"
    )
    elections = ["2025-05-01"]

    # By-election so maintaining exclusions from previous elections as comment for reference
    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if (
            uprn
            in [
                # "100062411430",  # CONNOLLY HOUSE, CONNOLLY WAY, CHICHESTER
                # "10090340673",  # FLAT, CO-OPERATIVE RETAIL SERVICES LTD, OLIVER WHITBY ROAD, CHICHESTER
                # "10008884574",  # PADDOCK HOUSE, PLAISTOW ROAD, LOXWOOD, BILLINGSHURST
                # "10002469404",  # NEWLANDS COTTAGE, LINCHMERE, HASLEMERE
                # "10008887597",  # THE GRANARY UPWALTHAM HOUSE FARM CHURCH FARM LANE, UPWALTHAM
                # "200001740959",  # BADGERS, BORDER CLOSE, HILL BROW, LISS
                # "10002467828",  # PALFREY FARM, LONDON ROAD, PETWORTH
                # "10014107960",  # HORSESHOE HOUSE, HENLEY HILL, HENLEY, HASLEMERE
                # "100061753348",  # GIG HOUSE, STUBCROFT LANE, EAST WITTERING, CHICHESTER
            ]
        ):
            return None

        if record.addressline6 in [
            # split
            "GU29 9QT",
            #  suspect
            # "PO20 8NX",
            # "PO20 8SP",
        ]:
            return None

        return super().address_record_to_dict(record)
