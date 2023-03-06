from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HAT"
    addresses_name = (
        "2023-05-04/2023-03-06T14:01:01.740038/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-06T14:01:01.740038/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200000999587",  # HOOK CROSS COTTAGE READING ROAD, ROTHERWICK, HOOK
            "100060420959",  # SHAPLEY LODGE, LONDON ROAD, HARTLEY WINTNEY, HOOK
            "10008960932",  # ANNEXE, SHAPLEY LODGE, LONDON ROAD, HARTLEY WINTNEY, HOOK
            "100060417933",  # STILLERS FARM, EWSHOT LANE, EWSHOT, FARNHAM
            "200001011509",  # WILLOW HOUSE, ALBANY ROAD, FLEET
            "10008963593",  # 1 OAKTREE PADDOCK, POTBRIDGE, ODIHAM, HOOK
            "10008963594",  # 2 OAKTREE PADDOCK POTBRIDGE ROAD, ODIHAM, HOOK
        ]:
            return None

        if record.addressline6 in [
            "GU52 0AF",  # splits
            "RG27 9RJ",  # splits
            "GU14 0LL",  # 128-130 OLD IVELY ROAD, FARNBOROUGH
        ]:
            return None

        return super().address_record_to_dict(record)
