from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "TEN"
    addresses_name = (
        "2023-05-04/2023-04-12T10:02:51.779215/Democracy Club - Polling Districts.tsv"
    )
    stations_name = (
        "2023-05-04/2023-04-12T10:02:51.779215/Democracy Club - Polling Stations.tsv"
    )
    elections = ["2023-05-04"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10094248268",  # 43 MIDDLETON MEWS, BRIGHTLINGSEA, COLCHESTER
        ]:
            return None

        if record.postcode in [
            # split
            "CO13 0FZ",
            "CO16 9UQ",
            "CO15 7AP",
            "CO14 8GH",
        ]:
            return None

        return super().address_record_to_dict(record)
