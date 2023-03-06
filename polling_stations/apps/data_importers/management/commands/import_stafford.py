from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "STA"
    addresses_name = "2023-05-04/2023-03-06T15:50:30.879822/Eros_SQL_Output012.csv"
    stations_name = "2023-05-04/2023-03-06T15:50:30.879822/Eros_SQL_Output012.csv"
    elections = ["2023-05-04"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "200001329430",  # ENSON HOUSE, ENSON, STAFFORD
            "10023358709",  # BEACON CROFT, BEACON FARM, BEACONSIDE, STAFFORD
            "10023356767",  # TUDOR HOUSE ADJ TO 8 NEWPORT ROAD, WOOTTON, ECCLESHALL
        ]:
            return None

        if record.housepostcode in ["ST17 0NU", "ST21 6AN", "ST21 6BE"]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Wedgwood Cricket Club Barlaston Park Barlaston Stoke on Trent ST12 9ES
        if (record.pollingstationnumber, record.pollingstationpostcode) == (
            "1",
            "ST12 9ES",
        ):
            record = record._replace(pollingstationpostcode="ST12 9ER")

        return super().station_record_to_dict(record)
