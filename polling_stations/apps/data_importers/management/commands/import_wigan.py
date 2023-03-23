from data_importers.management.commands import BaseXpressWebLookupCsvImporter


class Command(BaseXpressWebLookupCsvImporter):
    council_id = "WGN"
    addresses_name = "2023-05-04/2023-03-23T15:30:38.891498/PropertyPostCodePollingStationWebLookup-2023-03-23.CSV"
    stations_name = "2023-05-04/2023-03-23T15:30:38.891498/PropertyPostCodePollingStationWebLookup-2023-03-23.CSV"
    elections = ["2023-05-04"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10095422568",  # 2 ELDERFIELD, WORSLEY, MANCHESTER
            "200002861926",  # THE COTTAGE, SANDY LANE, HINDLEY, WIGAN
            "100012500668",  # DODHURST BROW FARM, SANDY LANE, HINDLEY, WIGAN
            "10009207679",  # 2A NORLEY HALL AVENUE, WIGAN
            "100011823007",  # 165 WIGAN ROAD, ASHTON-IN-MAKERFIELD, WIGAN
        ]:
            return None

        if record.postcode in [
            # splits
            "WN1 2QL",
            "WN1 2PQ",
            "WN7 1LU",
            "WN7 2BL",
            "WN6 7NZ",
            "WA3 3UJ",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # St Aidans Parish Centre, Highfield Grange Ave, Winstanley, Wigan, WN3 6EE
        if record.pollingplaceid == "9100":
            record = record._replace(
                pollingplaceeasting="355847", pollingplacenorthing="402852"
            )

        # Standish Community Centre, Moody Street, Off Church, Street Standish, WN6 0JY
        if record.pollingplaceid == "8982":
            record = record._replace(
                pollingplaceeasting="356374", pollingplacenorthing="410043"
            )

        return super().station_record_to_dict(record)
