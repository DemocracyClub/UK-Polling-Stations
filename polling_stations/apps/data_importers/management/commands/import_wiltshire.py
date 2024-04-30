from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WIL"
    addresses_name = (
        "2024-05-02/2024-04-30T08:22:02.367729/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-04-30T08:22:02.367729/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10094306546",  # MAREEBA, CARISBROOKE STUD, WEST SOLEY, CHILTON FOLIAT, HUNGERFORD
            "100121330656",  # 77 BOURNE AVENUE, SALISBURY
        ]:
            return None

        if record.addressline6 in [
            # split
            "SN10 4AD",
            "SP5 1RN",
            "SN14 6HT",
            "SN10 2PA",
            "SN8 1QB",
            "SP5 2NL",
            "SP3 6DY",
            "BA12 7JH",
            "SN8 1HG",
            "SN15 5JL",
            # suspect
            "SN16 0HT",
            "BA14 8RA",
            "SN15 4EU",
            "SN15 4EX",
        ]:
            return None

        return super().address_record_to_dict(record)
