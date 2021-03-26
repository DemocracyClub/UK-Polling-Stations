from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "KEC"
    addresses_name = "2021-03-24T11:28:23.977778/RBKC Democracy_Club__06May2021.CSV"
    stations_name = "2021-03-24T11:28:23.977778/RBKC Democracy_Club__06May2021.CSV"
    elections = ["2021-05-06"]

    def address_record_to_dict(self, record):
        if record.addressline6 in ["W11 4HD", "W14 8BA", "SW1X 9SG", "SW3 5RP"]:
            return None

        uprn = record.property_urn.strip().lstrip("0")
        if uprn in [
            "217130227",  # BASEMENT AND GROUND FLOOR FLAT 20 TREGUNTER ROAD, LONDON
        ]:
            return None

        if uprn == "217108045":
            record = record._replace(addressline6="W8 5DH")
        if (
            record.addressline6 == "W11 4LY"
            and record.addressline1 == "2B Drayson Mews"
        ):
            record = record._replace(addressline6="W8 4LY")
        return super().address_record_to_dict(record)
