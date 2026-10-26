from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RDG"
    addresses_name = (
        "2026-11-26/2026-10-26T10:19:11.827115/Democracy_Club__26November2026.tsv"
    )
    stations_name = (
        "2026-11-26/2026-10-26T10:19:11.827115/Democracy_Club__26November2026.tsv"
    )
    elections = ["2026-11-26"]
    csv_delimiter = "\t"

    # maintaining tweaks as comments through by-election

    # def address_record_to_dict(self, record):
    #     uprn = record.property_urn.strip().lstrip("0")

    #     if uprn in [
    #         "310051073",  # 221 BASINGSTOKE ROAD, READING
    #         "310008722",  # 64 ALEXANDRA ROAD, READING
    #         "310057403",  # 66 ALEXANDRA ROAD, READING
    #         "310064645",  # 1 STAR ROAD, CAVERSHAM, READING
    #     ]:
    #         return None

    #     if record.addressline6 in [
    #         # split
    #         "RG30 3NB",
    #         "RG30 4RX",
    #     ]:
    #         return None
    #     return super().address_record_to_dict(record)
