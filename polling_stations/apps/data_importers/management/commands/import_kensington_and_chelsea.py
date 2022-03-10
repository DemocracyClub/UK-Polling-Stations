from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "KEC"
    addresses_name = (
        "2022-05-05/2022-03-10T11:16:41.646308/Democracy_Club__05May2022.CSV"
    )
    stations_name = (
        "2022-05-05/2022-03-10T11:16:41.646308/Democracy_Club__05May2022.CSV"
    )
    elections = ["2022-05-05"]

    def address_record_to_dict(self, record):
        if record.addressline6 in [
            "SW1X 9SG",
            "SW7 4DW",
            "W11 4JJ",
            "W11 4HD",
        ]:
            return None

        uprn = record.property_urn.strip().lstrip("0")
        if uprn in [
            "217113295",  # DOCTORS SURGERY, 12 RADDINGTON ROAD, LONDON
            "217130227",  # BASEMENT AND GROUND FLOOR FLAT 20 TREGUNTER ROAD, LONDON
        ]:
            return None

        return super().address_record_to_dict(record)
