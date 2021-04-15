from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "ROS"
    addresses_name = "2021-03-26T12:03:10.152976/Democracy_Club__06May2021.tsv"
    stations_name = "2021-03-26T12:03:10.152976/Democracy_Club__06May2021.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10014333480",  # HEIGHT END COTTAGE HEIGHT END FARM BACUP OLD ROAD, BACUP
        ]:
            return None

        if record.addressline6 in [
            "OL12 8NU",
            "BB4 4NZ",
            "OL13 9BT",
            "BB4 7TD",
            "BB4 8TT",
            "OL13 0QR",
            "OL13 9QA",
            "BB4 9UD",
            "BB4 9LR",
            "BB4 7ND",
            "OL13 0PS",
            "BB4 9QR",
        ]:
            return None

        return super().address_record_to_dict(record)
