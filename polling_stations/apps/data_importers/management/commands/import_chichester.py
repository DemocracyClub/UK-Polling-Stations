from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "CHI"
    addresses_name = (
        "2023-05-04/2023-03-09T13:52:01.572585/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-09T13:52:01.572585/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100062411430",  # CONNOLLY HOUSE, CONNOLLY WAY, CHICHESTER
            "10090340673",  # FLAT, CO-OPERATIVE RETAIL SERVICES LTD, OLIVER WHITBY ROAD, CHICHESTER
            "10008884574",  # PADDOCK HOUSE, PLAISTOW ROAD, LOXWOOD, BILLINGSHURST
            "10002469404",  # NEWLANDS COTTAGE, LINCHMERE, HASLEMERE
            "10008887597",  # THE GRANARY UPWALTHAM HOUSE FARM CHURCH FARM LANE, UPWALTHAM
        ]:
            return None

        if record.addressline6 in [
            # split
            "PO20 9AD",
            "RH20 1PW",
            "PO19 3PX",
            "PO18 0PR",
            "PO18 8QG",
            "PO19 7QL",
            "GU28 9LY",
            "GU29 9QT",
            "GU28 0LD",
            # wrong
            "PO18 9AE",
            "PO18 9AF",
        ]:
            return None

        return super().address_record_to_dict(record)
