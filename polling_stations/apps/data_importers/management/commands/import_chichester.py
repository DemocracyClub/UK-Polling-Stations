from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CHI"
    addresses_name = "2024-07-04/2024-05-29T08:24:22.907129/chichester_combined.csv"
    stations_name = "2024-07-04/2024-05-29T08:24:22.907129/chichester_combined.csv"
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100062411430",  # CONNOLLY HOUSE, CONNOLLY WAY, CHICHESTER
            "10090340673",  # FLAT, CO-OPERATIVE RETAIL SERVICES LTD, OLIVER WHITBY ROAD, CHICHESTER
            "10008884574",  # PADDOCK HOUSE, PLAISTOW ROAD, LOXWOOD, BILLINGSHURST
            "10002469404",  # NEWLANDS COTTAGE, LINCHMERE, HASLEMERE
            "10008887597",  # THE GRANARY UPWALTHAM HOUSE FARM CHURCH FARM LANE, UPWALTHAM
            "200001740959",  # BADGERS, BORDER CLOSE, HILL BROW, LISS
            "10002467828",  # PALFREY FARM, LONDON ROAD, PETWORTH
            "10014107960",  # HORSESHOE HOUSE, HENLEY HILL, HENLEY, HASLEMERE
            "100061753348",  # GIG HOUSE, STUBCROFT LANE, EAST WITTERING, CHICHESTER
        ]:
            return None

        if record.addressline6 in [
            # split
            "PO18 0PR",
            "PO19 3PX",
            "GU29 9QT",
            "PO18 0PR",
            "PO18 8QG",
            "GU28 0LD",
            "RH20 1PW",
            "PO20 9AD",
            "PO19 7QL",
            #  suspect
            "PO20 8NX",
            "PO20 8SP",
        ]:
            return None

        return super().address_record_to_dict(record)
