from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter
from django.contrib.gis.geos import Point


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "NWP"
    addresses_name = "2024-07-04/2024-06-11T15:59:02.475355/Democracy_Club__04July2024.tsvClub__04July2024.tsv"
    stations_name = "2024-07-04/2024-06-11T15:59:02.475355/Democracy_Club__04July2024.tsvClub__04July2024.tsv"
    elections = ["2024-07-04"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def address_record_to_dict(self, record):
        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10093295441",  # TY TERNION, LODGE ROAD, CAERLEON, NEWPORT
            "10002155274",  # ORCHARD FARM, ST. BRIDES WENTLOOGE, NEWPORT
            "10002155651",  # BLUEBELL COTTAGE, ST. BRIDES WENTLOOGE, NEWPORT
            "100100646081",  # GREENFIELD HOUSE, TYLA LANE, OLD ST. MELLONS, CARDIFF
            "100100646082",  # GEM COTTAGE, TYLA LANE, OLD ST. MELLONS, CARDIFF
            "10002147773",  # WERN FARM, RHIWDERIN, NEWPORT
            "10014126660",  # MAISONETTE SECOND AND THIRD FLOOR 46 COMMERCIAL STREET, NEWPORT
            "10090277060",  # 6C TURNER STREET, NEWPORT
            "10090277061",  # 6B TURNER STREET, NEWPORT
            "10090277062",  # 6A TURNER STREET, NEWPORT
            "10010553788",  # 39 REMBRANDT WAY, NEWPORT
            "10002153590",  # RED ROBIN HOUSE, LLANDEVAUD, NEWPORT
            "10002153795",  # WOODLAND VIEW, PENHOW, CALDICOT
            "100100668792",  # YEW TREE COTTAGE, HENDREW LANE, LLANDEVAUD, NEWPORT
            "10002153732",  # SEYMOUR LODGE, PENHOW, CALDICOT
            "10002153780",  # HOLLY TREE COTTAGE, PENHOW, CALDICOT
            "10002153746",  # SEYMOUR COTTAGE, PENHOW, CALDICOT
            "10002153749",  # GROES WEN COTTAGE, PENHOW, CALDICOT
            "10014125572",  # MANAGERS ACCOMMODATION GROES WEN INN CHEPSTOW ROAD, NEWPORT
            "10093295775",  # THE OLD GARDEN, PONTYMASON LANE, ROGERSTONE, NEWPORT
            "100100654808",  # FIRST FLOOR FLAT 193 CARDIFF ROAD, NEWPORT
            "10014126369",  # FLAT 1 80-81 COMMERCIAL ROAD, NEWPORT
        ]:
            return None

        if record.post_code in [
            "NP10 8NT",  # split
            # suspect
            "NP10 8AT",
            "NP20 1LQ",
            "NP20 1HY",
            "NP20 7DY",
            "NP19 8AY",
            "NP20 3AF",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Just Dance, Locke Street Community Centre, 8 Queens Hill, Newport, NP20 5HJ
        if record.polling_place_id == "13471":
            record = record._replace(polling_place_postcode="NP20 5HL")

        rec = super().station_record_to_dict(record)

        # Cefn Wood Baptist Church, Ebenezer Drive, Rogerstone, Newport, NP10 9DP
        if rec["internal_council_id"] == "13703":
            rec["location"] = Point(327492, 187872, srid=27700)
            return rec

        return super().station_record_to_dict(record)
