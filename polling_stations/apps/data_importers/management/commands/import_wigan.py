from data_importers.management.commands import BaseXpressWebLookupCsvImporter


class Command(BaseXpressWebLookupCsvImporter):
    council_id = "WGN"
    addresses_name = "2021-04-06T12:29:53.599045/democracy club wigan council.tsv"
    stations_name = "2021-04-06T12:29:53.599045/democracy club wigan council.tsv"
    elections = ["2021-05-06"]
    csv_delimiter = "\t"
    csv_encoding = "windows-1252"

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "100012498804",  # THE CHANTERS CARE HOME, TYLDESLEY OLD ROAD, ATHERTON, MANCHESTER
        ]:
            return None

        if record.postcode in [
            "WN7 2BL",
            "WN2 4NE",
            "WN6 7NZ",
            "WN1 2PQ",
            "WN1 2QL",
            "M46 0EJ",
            "WN7 5FS",
            "WA3 3EY",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):

        # Standish Community Centre Moody Street Off Church Street Standish WN6 0JY
        if record.pollingplaceid == "7469":
            record = record._replace(pollingplaceeasting="")
            record = record._replace(pollingplacenorthing="")

        return super().station_record_to_dict(record)
