from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "LIC"
    addresses_name = (
        "2025-05-01/2025-02-26T16:59:12.325060/SupportSql_20250226_132609.tsv"
    )
    stations_name = (
        "2025-05-01/2025-02-26T16:59:12.325060/SupportSql_20250226_132609.tsv"
    )
    elections = ["2025-05-01"]
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "235056965",  # FLAT CROWN AND ARROWS MOORLAND AVENUE, LINCOLN
        ]:
            return None

        if record.housepostcode in [
            # split
            "LN5 8AG",
            "LN6 8DB",
            "LN1 1BU",
            "LN2 4DY",
            "LN1 1QD",
            "LN5 7LA",
            "LN2 4NA",
            "LN6 0LH",
            "LN2 5EJ",
            "LN1 1DR",
            "LN6 8AZ",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # removes wrong UPRN for: St Peter in Eastgate Church, Eastgate, Lincoln, LN2 4AA
        if self.get_station_hash(record) == "13-st-peter-in-eastgate-church":
            record = record._replace(pollingvenueuprn="")

        return super().station_record_to_dict(record)
