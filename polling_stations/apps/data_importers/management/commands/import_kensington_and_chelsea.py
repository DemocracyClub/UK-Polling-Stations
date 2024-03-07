from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "KEC"
    addresses_name = (
        "2024-05-02/2024-03-07T14:43:23.540506/Democracy_Club__02May2024.tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-07T14:43:23.540506/Democracy_Club__02May2024.tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            # split
            "SW7 4DW",
            "W11 4HD",
            "W11 4JJ",
            "SW3 3LA",
        ]:
            return None

        uprn = record.property_urn.strip().lstrip("0")
        if uprn in [
            "217113295",  # DOCTORS SURGERY, 12 RADDINGTON ROAD, LONDON
            "217130227",  # BASEMENT AND GROUND FLOOR FLAT 20 TREGUNTER ROAD, LONDON
            "217016105",  # 4 CLAREVILLE GROVE, LONDON
        ]:
            return None

        return super().address_record_to_dict(record)
