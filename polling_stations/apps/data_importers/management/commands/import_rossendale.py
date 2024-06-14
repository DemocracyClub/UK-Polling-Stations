from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "ROS"
    addresses_name = (
        "2024-07-04/2024-06-14T15:07:26.266331/Democracy_Club__04July2024 (29).tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-14T15:07:26.266331/Democracy_Club__04July2024 (29).tsv"
    )
    elections = ["2024-07-04"]
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
