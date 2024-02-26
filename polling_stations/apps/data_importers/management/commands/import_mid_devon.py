from data_importers.management.commands import BaseXpressWebLookupCsvImporter


class Command(BaseXpressWebLookupCsvImporter):
    council_id = "MDE"
    addresses_name = "2024-05-02/2024-02-26T12:46:32.302333/PropertyPostCodePollingStationWebLookup-2024-02-26 MID DEVON.TSV"
    stations_name = "2024-05-02/2024-02-26T12:46:32.302333/PropertyPostCodePollingStationWebLookup-2024-02-26 MID DEVON.TSV"
    elections = ["2024-05-02"]
    csv_delimiter = "\t"

    def station_record_to_dict(self, record):
        # Chawleigh Jubilee Hall, Chawleigh
        if record.pollingplaceid == "11109":
            record = record._replace(pollingplaceeasting="", pollingplacenorthing="")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10024639781",  # FOXHOLES FARM, CLAYHIDON, CULLOMPTON
            "10002162361",  # POTTERS, SHILLINGFORD, TIVERTON
            "200004004367",  # CARAVANS 3 AND 4 THREE ACRES UFFCULME ROAD, WILLAND
            "200004004366",  # CARAVANS 1 AND 2 THREE ACRES UFFCULME ROAD, WILLAND
            "10009448630",  # MAYFIELD HOUSE, TEMPLETON, TIVERTON
            "10002165647",  # POUND CASTLE, BICKLEIGH, TIVERTON
            "10095581422",  # OAKLEIGH BARN, BICKLEIGH, TIVERTON
            "200004005422",  # GUNSTONE LODGE GUNSTONE PARK ROAD FROM GUNSTONE CROSS TO GUNSTONE MILL CROSS, GUNSTONE
            "200004006381",  # GUNSTONE PARK, GUNSTONE, CREDITON
            "10093538401",  # COPSTONE HOUSE, BLACK DOG, CREDITON
            "10009451330",  # TOADYPARK, ZEAL MONACHORUM, CREDITON
            "10093538015",  # HIGHER POND BARN, KEYMELFORD, YEOFORD, CREDITON
            "10002162357",  # RADDS COTTAGE, CALVERLEIGH, TIVERTON
        ]:
            return None

        if record.postcode in [
            # look wrong
            "EX16 8RA",
        ]:
            return None

        return super().address_record_to_dict(record)
