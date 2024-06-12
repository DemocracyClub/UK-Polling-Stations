from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "RDG"
    addresses_name = (
        "2024-07-04/2024-06-12T11:03:00.786314/Democracy_Club__04July2024 2 (1).tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-12T11:03:00.786314/Democracy_Club__04July2024 2 (1).tsv"
    )
    elections = ["2024-07-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "310084858",  # FLAT 3, 69 NORTHUMBERLAND AVENUE, READING
            "310084857",  # FLAT 2, 69 NORTHUMBERLAND AVENUE, READING
            "310051073",  # 221 BASINGSTOKE ROAD, READING
            "310008722",  # 64 ALEXANDRA ROAD, READING
            "310057403",  # 66 ALEXANDRA ROAD, READING
            "310064645",  # 1 STAR ROAD, CAVERSHAM, READING
            "310084858",  # FLAT 3, 69 NORTHUMBERLAND AVENUE, READING
            "310084857",  # FLAT 2, 69 NORTHUMBERLAND AVENUE, READING
        ]:
            return None

        if record.addressline6 in [
            # split
            "RG30 3NB",
            "RG30 4RX",
        ]:
            return None
        return super().address_record_to_dict(record)
