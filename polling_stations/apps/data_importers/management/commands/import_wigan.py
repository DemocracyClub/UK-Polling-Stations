from data_importers.management.commands import BaseXpressWebLookupCsvImporter


class Command(BaseXpressWebLookupCsvImporter):
    council_id = "WGN"
    addresses_name = "2022-05-05/2022-04-07T12:02:19.829718/PropertyPostCodePollingStationWebLookup-2022-04-07.TSV"
    stations_name = "2022-05-05/2022-04-07T12:02:19.829718/PropertyPostCodePollingStationWebLookup-2022-04-07.TSV"
    elections = ["2022-05-05"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):

        if record.postcode in [
            "WN7 2BL",
            "WN6 7NZ",
            "WN1 2PQ",
            "WN1 2QL",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):

        if record.pollingplaceid in [
            "7863",  # Standish Community Centre Moody Street Off Church Street Standish WN6 0JY
            "7848",  # Shevington Youth Club, Highfield Avenue
        ]:
            record = record._replace(pollingplaceeasting="")
            record = record._replace(pollingplacenorthing="")

        return super().station_record_to_dict(record)
