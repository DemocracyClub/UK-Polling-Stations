from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "ROS"
    addresses_name = (
        "2022-05-05/2022-03-02T14:17:20.976699/Democracy_Club__05May2022.tsv"
    )
    stations_name = (
        "2022-05-05/2022-03-02T14:17:20.976699/Democracy_Club__05May2022.tsv"
    )
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):

        if record.addressline6 in [
            "BB4 8TT",
            "OL13 0QR",
            "BB4 9QR",
        ]:
            return None

        return super().address_record_to_dict(record)
