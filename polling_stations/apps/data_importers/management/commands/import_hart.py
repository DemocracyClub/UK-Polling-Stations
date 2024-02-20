from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HAT"
    addresses_name = (
        "2024-05-02/2024-02-20T16:01:42.397817/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-02-20T16:01:42.397817/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "200000999587",  # HOOK CROSS COTTAGE READING ROAD, ROTHERWICK, HOOK
            "100060417933",  # STILLERS FARM, EWSHOT LANE, EWSHOT, FARNHAM
            "200001011509",  # WILLOW HOUSE, ALBANY ROAD, FLEET
            "10008963593",  # 1 OAKTREE PADDOCK, POTBRIDGE, ODIHAM, HOOK
            "10008963594",  # 2 OAKTREE PADDOCK POTBRIDGE ROAD, ODIHAM, HOOK
            "10008962564",  # BAILEYS FARMHOUSE, ODIHAM ROAD, ODIHAM, HOOK
        ]:
            return None

        if record.addressline6 in [
            # split
            "RG27 9RJ",
            "GU52 0AF",
        ]:
            return None

        return super().address_record_to_dict(record)
