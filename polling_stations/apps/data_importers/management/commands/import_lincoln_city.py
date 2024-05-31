from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "LIC"
    addresses_name = "2024-07-04/2024-05-31T11:04:59.933101/Eros_SQL_Output013.csv"
    stations_name = "2024-07-04/2024-05-31T11:04:59.933101/Eros_SQL_Output013.csv"
    elections = ["2024-07-04"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "235056965",  # FLAT CROWN AND ARROWS MOORLAND AVENUE, LINCOLN
        ]:
            return None

        if record.housepostcode in [
            # split
            "LN1 1BU",
            "LN1 1DR",
            "LN1 1QD",
            "LN2 4DY",
            "LN2 4NA",
            "LN2 5EJ",
            "LN5 7LA",
            "LN5 8AG",
            "LN6 0LH",
            "LN6 7UY",
            "LN6 8AZ",
            "LN6 8DB",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # removes wrong UPRN for: St Peter in Eastgate Church, Eastgate, Lincoln, LN2 4AA
        if record.pollingvenueid == "52":
            record = record._replace(pollingvenueuprn="")

        return super().station_record_to_dict(record)
