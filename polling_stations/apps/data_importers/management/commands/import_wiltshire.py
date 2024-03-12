from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "WIL"
    addresses_name = (
        "2024-05-02/2024-03-12T12:43:46.443661/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-12T12:43:46.443661/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10094306546",  # MAREEBA, CARISBROOKE STUD, WEST SOLEY, CHILTON FOLIAT, HUNGERFORD
        ]:
            return None
        if record.addressline6 in [
            # split
            "SP5 2NL",
            "SN10 4AD",
            "SP5 1RN",
            "SN8 1HG",
            "SN10 2PA",
            "SP3 6DY",
            "SN8 1QB",
            "SN15 5JL",
            "SN14 6HT",
            # suspect
            "SN16 0HT",
            "BA14 8RA",
        ]:
            return None
        return super().address_record_to_dict(record)
