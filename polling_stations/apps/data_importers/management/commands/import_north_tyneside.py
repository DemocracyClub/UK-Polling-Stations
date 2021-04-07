from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NTY"
    addresses_name = (
        "2021-03-22T11:03:37.869995/North Tyneside Democracy_Club__06May2021.tsv"
    )
    stations_name = (
        "2021-03-22T11:03:37.869995/North Tyneside Democracy_Club__06May2021.tsv"
    )
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "47080850",  # FLAT ABOVE ALNWICK CASTLE SAVILLE STREET, NORTH SHIELDS
            "47057152",  # LOW LIGHT HOUSE, FISH QUAY, NORTH SHIELDS
            "47036550",  # FLAT AT 1 FRONT STREET, CHIRTON, NORTH SHIELDS
        ]:
            return None

        if record.addressline6 in ["NE12 8EE", "NE27 0XP"]:
            return None

        return super().address_record_to_dict(record)
