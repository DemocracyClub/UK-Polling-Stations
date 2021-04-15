from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "AGY"
    addresses_name = (
        "2021-03-29T13:38:58.901511/Anglesey polling_station_export-2021-03-29.csv"
    )
    stations_name = (
        "2021-03-29T13:38:58.901511/Anglesey polling_station_export-2021-03-29.csv"
    )
    elections = ["2021-05-06"]

    def station_record_to_dict(self, record):
        if record.pollingstationnumber == "22":
            # NEUADD BENTREF LLANFACHRAETH, LLANFACHRAETH, YNYS MON
            # Is LL65 2UH; should probably be LL65 4UL, but let's not guess
            record = record._replace(pollingstationpostcode="")

        if record.pollingstationnumber == "21":
            # YSGOLDY CAPEL M C CARMEL CARMEL
            # Postcode isn't actually in Carmel, and not within polling area
            record = record._replace(pollingstationpostcode="")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.housepostcode in [
            "LL65 1NU",
            "LL65 1BG",
            "LL65 2ED",
            "LL65 2EL",
            "LL65 3SE",
            "LL72 8LJ",
            "LL74 8ST",
        ]:
            return None  # split

        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "200002650495",  # suspicious distance, overlap
            "200002649098",  # suspicious distance, overlap
            "10013457915",  # suspicious distance, overlap
        ]:
            return None

        return super().address_record_to_dict(record)
