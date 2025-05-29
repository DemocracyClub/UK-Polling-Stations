from data_importers.management.commands import BaseShpStationsShpDistrictsImporter
from textwrap import dedent


class Command(BaseShpStationsShpDistrictsImporter):
    council_id = "WLL"
    districts_name = "2025-05-20/NEWPD2025.shp"
    stations_name = "2025-05-20/PS2025.shp"
    elections = []

    def district_record_to_dict(self, record):
        if record[1] == "PEL4AB":
            return {"internal_council_id": "PEL4/AB", "name": "PEL4/AB"}
        if record[1] == "ASC5/AB":
            return {"internal_council_id": "ACS5/AB", "name": "ACS5/AB"}
        return {"internal_council_id": record[1], "name": record[1]}

    def station_record_to_dict(self, record):
        if "\n" in record[0]:
            ward_name = record[0].split("\n")[0].strip()
        else:
            ward_name = record[0].strip()
        if "(" in ward_name:
            ward_name = ward_name.split("(")[0].strip()

        alt_address = None

        address_text = dedent(f"""
        Starting from May 2026

        Your new ward will be: **{ward_name}**

        Your new polling district will be: **{record[1]}**""")

        if record[1] == "STM3/WB" and record[4] == "Option 2":
            return None
        if record[1] == "STM3/WB" and record[4] == "Option 1":
            alt_address = "Walsall Gala Swimming & Fitness Centre, Gala Swimming Baths, Tower Street WS1 1DH"

        if record[1] == "PLK1/WB" and record[4] == "Option 2":
            return None
        if record[1] == "PLK1/WB" and record[4] == "Option 1":
            alt_address = "Alternative - Emmanuel School, 36 Wolverhampton Road WS2 8PR"

        if record[1] == "RSF1/AB" and record[4] == "Option 2":
            return None
        if record[1] == "RSF1/AB" and record[4] == "Option 1":
            alt_address = (
                "Alternative - Shelfield Methodist Church, 77 Lichfield Road WS4 1PU"
            )

        if alt_address:
            address_text += dedent(f"""

            Your new polling station will be either:

            <address>{'<br>'.join(record[3].split(','))}</address>

            or

            <address>{'<br>'.join(alt_address.split(','))}</address>""")
        else:
            address_text += dedent(f"""

            Your new polling station will be:

            <address>{'<br>'.join(record[3].split(','))}</address>""")

        station_dict = {
            "internal_council_id": record[1],
            "address": address_text.strip(),
            "postcode": "",
            "polling_district_id": record[1],
        }
        if alt_address:
            station_dict["location"] = None
        return station_dict
