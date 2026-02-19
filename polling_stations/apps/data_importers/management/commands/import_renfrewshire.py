from addressbase.models import UprnToCouncil
from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "RFW"
    addresses_name = "2026-05-07/2026-02-19T12:45:14.327541/Democracy Club - Polling District (Ren).csv"
    stations_name = "2026-05-07/2026-02-19T12:45:14.327541/Democracy Club - Polling Stations (Ren).csv"
    elections = ["2026-05-07"]
    csv_encoding = "utf-16le"

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
            if record.uprn in council_uprns:
                self.COUNCIL_STATIONS.add(record.stationcode)

    def address_record_to_dict(self, record):
        if record.stationcode not in self.COUNCIL_STATIONS:
            return None

        if record.postcode in (
            # splits
            "PA4 8YX",
            "PA2 8BF",
            "PA12 4DL",
            "PA4 8DB",
            "PA6 7HT",
            "PA3 2QT",
            "PA2 6QJ",
            "PA6 7LH",
            "PA5 8YP",
            "PA1 2JL",
        ):
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        if record.stationcode not in self.COUNCIL_STATIONS:
            return None

        # removes name duplication
        record = record._replace(add1="")

        # Add missing point for: Tweedie Hall Ardlamont Square, Linwood, Paisley, Renfrewshire, PA3 3DE
        if record.stationcode in ("SW11 - JOHNSTH_1", "SW11 - JOHNSTH_2"):
            record = record._replace(xordinate="242727", yordinate="663077")

        # Add missing point for: Johnstone Town Hall, 25 Church Street, Johnstone, PA5 8EG
        if record.stationcode in ("SW17 - TWEED_1", "SW17 - TWEED_2", "SW17 - TWEED_3"):
            record = record._replace(xordinate="244307", yordinate="664395")

        # HOUSTON & KILLELLAN CHURCH HALLS location
        # https://app.asana.com/0/1207538772343223/1207727040327547/f
        if record.stationcode in (
            "IW01A - HOUSTKK_1",
            "IW01A - HOUSTKK_2",
            "IW01A - HOUSTKK_3",
            "IW01B - HOUSTKK_4",
            "IW01B - HOUSTKK_5",
        ):
            record = record._replace(xordinate="240494", yordinate="666785")

        return super().station_record_to_dict(record)
