from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CHI"

    addresses_name = (
        "2021-03-08T20:23:52.964809/Chichester Democracy_Club__06May2021.tsv"
    )
    stations_name = (
        "2021-03-08T20:23:52.964809/Chichester Democracy_Club__06May2021.tsv"
    )
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10093115403",  # 1 BLOMFIELD DRIVE, CHICHESTER
            "100062411430",  # CONNOLLY HOUSE, CONNOLLY WAY, CHICHESTER
            "100062410959",  # MUCHOS NACHOS, 140 WHYKE ROAD, CHICHESTER
            "10090340673",  # FLAT, CO-OPERATIVE RETAIL SERVICES LTD, OLIVER WHITBY ROAD, CHICHESTER
            "10008884574",  # PADDOCK HOUSE, PLAISTOW ROAD, LOXWOOD, BILLINGSHURST
            "10002469404",  # NEWLANDS COTTAGE, LINCHMERE, HASLEMERE
            "200001740959",  # BADGERS, BORDER CLOSE, HILL BROW, LISS
            "10002470928",  # THE FORGE, HENLEY HILL, HENLEY, HASLEMERE
            "10008887597",  # THE GRANARY UPWALTHAM HOUSE FARM CHURCH FARM LANE, UPWALTHAM
        ]:
            return None

        if record.addressline6 in [
            "PO19 7QL",
            "RH20 1PW",
            "GU28 0LD",
            "GU29 9QT",
            "GU28 9LY",
            "PO20 9AD",
            "PO18 0PR",
            "PO19 8FT",
            "PO18 9AE",
            "RH14 0JY",
        ]:
            return None

        return super().address_record_to_dict(record)
