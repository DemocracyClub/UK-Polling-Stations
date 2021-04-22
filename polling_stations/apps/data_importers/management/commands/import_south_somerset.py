from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "SSO"
    addresses_name = "2021-03-17T11:59:50.337243/South Somerset polling_station_export-2021-03-17.csv"
    stations_name = "2021-03-17T11:59:50.337243/South Somerset polling_station_export-2021-03-17.csv"
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "30065145",  # HARE FARM, HARE LANE, BUCKLAND ST. MARY, CHARD
            "30127709",  # MOBILE HOME AT OAK VIEW FARM HARE LANE, BUCKLAND ST MARY, CHARD
            "30095367",  # ST. MARYS HOUSE, WEST COKER HILL, WEST COKER, YEOVIL
            "30515573",  # GRANGE FARM, BOWDEN, HENSTRIDGE, TEMPLECOMBE
            "30105103",  # THE ORCHARD FARMHOUSE, STOWELL, SHERBORNE
        ]:
            return None

        if record.housepostcode in [
            "TA20 2BE",
            "TA14 6TS",
            "TA10 0QH",
            "BA10 0BU",
            "TA10 0DL",
            "TA3 6RP",
            "BA9 9NZ",
            "BA21 5DX",
        ]:
            return None

        return super().address_record_to_dict(record)
