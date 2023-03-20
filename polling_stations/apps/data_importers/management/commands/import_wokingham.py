from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WOK"
    addresses_name = (
        "2023-05-04/2023-03-20T16:45:40.415434/Democracy_Club__04May2023.tsv"
    )
    stations_name = (
        "2023-05-04/2023-03-20T16:45:40.415434/Democracy_Club__04May2023.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "14013638",  # 116 ELM ROAD, EARLEY, READING
            "14013639",  # 118 ELM ROAD, EARLEY, READING
            "10024046704",  # 43 BROAD STREET, WOKINGHAM
        ]:
            return None

        if record.addressline6 in [
            "RG2 9LG",
            "RG6 4AG",
            "RG7 1NL",
            "RG7 1PS",  # BASINGSTOKE ROAD, SPENCERS WOOD, READING
        ]:
            return None

        return super().address_record_to_dict(record)
