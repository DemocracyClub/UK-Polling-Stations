from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "NEL"
    addresses_name = "2026-05-07/2026-03-11T15:10:52.914923/Democracy Club - Idox_2026-03-11 15-08.csv"
    stations_name = "2026-05-07/2026-03-11T15:10:52.914923/Democracy Club - Idox_2026-03-11 15-08.csv"
    elections = ["2026-05-07"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "10090078903",  # FLAT, 247 GRIMSBY ROAD, CLEETHORPES
        ]:
            return None

        if record.postcode in [
            # split
            "DN33 3PF",
            "DN35 0RA",
            # suspect
            "DN37 0BN",
        ]:
            return None
        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        if record.pollingvenueid == "19":
            # point for this one is in the North Sea
            # delete the grid ref and use UPRN instead
            record = record._replace(pollingvenueeasting="0")
            record = record._replace(pollingvenuenorthing="0")
        return super().station_record_to_dict(record)
