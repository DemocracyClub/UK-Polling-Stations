from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "NOW"
    addresses_name = (
        "2021-03-24T11:30:58.947611/Norwich new polling_station_export-2021-03-24.csv"
    )
    stations_name = (
        "2021-03-24T11:30:58.947611/Norwich new polling_station_export-2021-03-24.csv"
    )
    elections = ["2021-05-06"]
    csv_delimiter = ","

    def address_record_to_dict(self, record):
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "100091562008",  # 10 SPROWSTON ROAD, NORWICH
            "10093501268",  # 481D SPROWSTON ROAD, NORWICH
            "100091339250",  # FIRST FLOOR FLAT 70 SILVER ROAD, NORWICH
            "100090915857",  # 9 OAK STREET, NORWICH
            "100090915856",  # 7 OAK STREET, NORWICH
            "100090915855",  # 5 OAK STREET, NORWICH
            "100090915854",  # 3 OAK STREET, NORWICH
            "100090890924",  # 32 BRITANNIA ROAD, NORWICH
            "100090890926",  # 34 BRITANNIA ROAD, NORWICH
            "100090890928",  # 36 BRITANNIA ROAD, NORWICH
        ]:
            return None

        if record.housepostcode in ["NR2 3AT", "NR4 7FW"]:
            return None

        return super().address_record_to_dict(record)
