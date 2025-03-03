from addressbase.models import UprnToCouncil
from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "VAL"
    addresses_name = (
        "2025-05-01/2025-03-03T13:58:57.436476/Democracy_Club__01May2025 2.tsv"
    )
    stations_name = (
        "2025-05-01/2025-03-03T13:58:57.436476/Democracy_Club__01May2025 2.tsv"
    )
    elections = ["2025-05-01"]
    csv_encoding = "windows-1252"
    csv_delimiter = "\t"

    def pre_import(self):
        # We need to consider rows that don't have a uprn when importing data.
        # However there are lots of rows for other councils in this file.
        # So build a list of stations from rows that do have UPRNS
        # and then use that list of stations to make sure we check relevant rows, even if they don't have a UPRN

        council_uprns = set(
            UprnToCouncil.objects.filter(lad=self.council.geography.gss).values_list(
                "uprn", flat=True
            )
        )
        self.COUNCIL_STATIONS = set()
        data = self.get_addresses()

        for record in data:
            if record.property_urn in council_uprns:
                self.COUNCIL_STATIONS.add(record.polling_place_id)

    def station_record_to_dict(self, record):
        if record.polling_place_id not in self.COUNCIL_STATIONS:
            return None

        # Removing bad coords for:
        # Milton Hill Bowls Club, Potash Lane, Milton Hill, Abingdon OX14 4DR
        if record.polling_place_id == "23925":
            record = record._replace(
                polling_place_easting="",
                polling_place_northing="",
            )

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.polling_place_id not in self.COUNCIL_STATIONS:
            return None

        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10095813377",  # 2 BENEDICTINE ROW, ABINGDON
        ]:
            return None

        if record.addressline6 in [
            # split
            "SN7 8QH",
            "OX13 5GW",
            "OX13 5ND",
            "SN7 8DJ",
            # suspect
            "OX14 1TG",
            "OX14 1ZW",
            "OX11 6JY",
        ]:
            return None

        return super().address_record_to_dict(record)
