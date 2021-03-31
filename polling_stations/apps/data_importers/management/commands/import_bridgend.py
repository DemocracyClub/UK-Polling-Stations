from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "BGE"
    addresses_name = (
        "2021-03-17T10:33:16.382690/Bridgend polling_station_export-2021-03-16.csv"
    )
    stations_name = (
        "2021-03-17T10:33:16.382690/Bridgend polling_station_export-2021-03-16.csv"
    )
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "200002664482",  # YNYSLAS UCHAF FARM, BLACKMILL, BRIDGEND
            "200001775090",  # GLYNTAWEL HOUSE, PANT HIRWAUN, BRYNCETHIN, BRIDGEND
            "10013368189",  # BALLAS BARNS, HEOL Y SHEET, STORMY DOWN, PYLE, BRIDGEND
        ]:
            return None

        if record.housepostcode in [
            "CF31 1NP",
            "CF31 5FD",
            "CF34 0UF",
            "CF35 6HZ",
            "CF34 9BT",
            "CF34 0BF",
            "CF34 0DY",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Llangeinor RFC Llangeinor FC Bettws Road Llangeinor CF32 8FG
        if (record.pollingstationnumber, record.pollingstationpostcode) == (
            "52",
            "CF32 8FG",
        ):
            record = record._replace(pollingstationpostcode="")

        # Pyle Rugby Football Club Brynglas Terrace Pyle Bridgend CF36 6AG
        if (record.pollingstationnumber, record.pollingstationpostcode) == (
            "33",
            "CF36 6AG",
        ):
            record = record._replace(pollingstationpostcode="")

        return super().station_record_to_dict(record)
