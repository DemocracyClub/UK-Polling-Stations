from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "NOW"
    addresses_name = "2022-05-05/2022-04-22T09:23:53.485488/Democracy Club  - Polling districts export.csv"
    stations_name = "2022-05-05/2022-04-22T09:23:53.485488/Democracy Club  - Polling stations export v2.0.csv"
    elections = ["2022-05-05"]

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "100091562008",  # 10 SPROWSTON ROAD, NORWICH
            "10090481878",  # 141B UNTHANK ROAD, NORWICH
            "100090915857",  # 9 OAK STREET, NORWICH
            "100090915856",  # 7 OAK STREET, NORWICH
            "100090915855",  # 5 OAK STREET, NORWICH
            "100090915854",  # 3 OAK STREET, NORWICH
        ]:
            return None

        return super().address_record_to_dict(record)
