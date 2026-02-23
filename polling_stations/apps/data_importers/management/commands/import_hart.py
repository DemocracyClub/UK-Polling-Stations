from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "HAT"
    addresses_name = (
        "2026-05-07/2026-02-23T15:34:17.039702/Democracy_Club__07May2026.tsv"
    )
    stations_name = (
        "2026-05-07/2026-02-23T15:34:17.039702/Democracy_Club__07May2026.tsv"
    )
    elections = ["2026-05-07"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10008959754",  # LIVING ACCOMMODATION 82 LONDON ROAD, BLACKWATER, CAMBERLEY
            "10008957210",  # 98 ALDERSHOT ROAD, CHURCH CROOKHAM, FLEET
            "200000999587",  # HOOK CROSS COTTAGE READING ROAD, ROTHERWICK, HOOK
            "200001011509",  # WILLOW HOUSE, ALBANY ROAD, FLEET
            "10008963593",  # 1 OAKTREE PADDOCK, POTBRIDGE, ODIHAM, HOOK
            "10008963594",  # 2 OAKTREE PADDOCK POTBRIDGE ROAD, ODIHAM, HOOK
            "10008962564",  # BAILEYS FARMHOUSE, ODIHAM ROAD, ODIHAM, HOOK
        ]:
            return None

        if record.addressline6 in [
            # split
            "RG27 9RJ",
        ]:
            return None

        return super().address_record_to_dict(record)
