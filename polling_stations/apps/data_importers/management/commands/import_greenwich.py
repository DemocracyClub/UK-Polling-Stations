from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "GRE"
    addresses_name = (
        "2024-07-04/2024-06-10T12:05:14.810020/Democracy_Club__04July2024.tsv"
    )
    stations_name = (
        "2024-07-04/2024-06-10T12:05:14.810020/Democracy_Club__04July2024.tsv"
    )
    elections = ["2024-07-04"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "100020975456",  # 56A HILLREACH, LONDON
        ]:
            return None

        if record.addressline6 in [
            # splits
            "SE9 2BU",
            "SE3 9BT",
        ]:
            return None

        return super().address_record_to_dict(record)
