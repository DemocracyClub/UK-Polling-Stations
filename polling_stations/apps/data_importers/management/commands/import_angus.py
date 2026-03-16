from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "ANS"
    addresses_name = "2026-05-07/2026-03-16T10:43:33.402171/Democracy Club - Idox_2026-02-26 10-26.csv"
    stations_name = "2026-05-07/2026-03-16T10:43:33.402171/Democracy Club - Idox_2026-02-26 10-26.csv"
    elections = ["2026-05-07"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "117080095",  # LOWNIE HILL COTTAGE, FORFAR
            "117087696",  # WOODSIDE, NETHER TULLOES FARM, FORFAR
        ]:
            return None

        if record.postcode in [
            # splits
            "DD9 7EZ",
            "DD8 2SF",
            "DD8 4QB",
            "DD8 5PP",
            "DD8 2TJ",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # add missing postcode for: Glamis Heritage Education Centre, Glamis
        if record.pollingstationnumber == "80":
            record = record._replace(pollingstationpostcode="DD8 1RS")

        # add missing postcode for: Kingoldrum Village Hall, Kingoldrum
        if record.pollingstationnumber == "70":
            record = record._replace(pollingstationpostcode="DD8 5HW")

        return super().station_record_to_dict(record)
