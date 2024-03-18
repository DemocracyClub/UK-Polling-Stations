from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "ROS"
    addresses_name = (
        "2024-05-02/2024-03-18T15:46:48.192713/Democracy_Club__02May2024 (23).tsv"
    )
    stations_name = (
        "2024-05-02/2024-03-18T15:46:48.192713/Democracy_Club__02May2024 (23).tsv"
    )
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100010596064",  # 1 FERNHILL CLOSE, BACUP
            "100012410082",  # 1A ROCHDALE ROAD, RAMSBOTTOM, BURY
        ]:
            return None

        if record.addressline6 in [
            # splits
            "BB4 8TT",
        ]:
            return None

        return super().address_record_to_dict(record)
