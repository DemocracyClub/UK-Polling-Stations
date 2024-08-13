from addressbase.models import UprnToCouncil
from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "BDF"
    addresses_name = "2024-07-04/2024-06-23T08:29:48.894657/bdf-districts-combined.csv"
    stations_name = "2024-07-04/2024-06-23T08:29:48.894657/bdf-stations-combined.csv"
    elections = ["2024-07-04"]

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

    def station_record_to_dict(self, record):
        if record.stationcode not in self.COUNCIL_STATIONS:
            return None

        # BEDFORD HOSPITAL, BEDFORD HOSPITAL, KEMPSTON ROAD, BEDFORD, MK42 9DJ
        if record.pollingstationid == "12423":
            record = record._replace(xordinate="")
            record = record._replace(yordinate="")

        # bug report:
        # removes wrong point for stations at: PARK ROAD METHODIST CHURCH, PARK ROAD WEST, BEDFORD
        if record.stationcode in [
            "31",
            "32",
        ]:
            record = record._replace(xordinate="")
            record = record._replace(yordinate="")
        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.stationcode not in self.COUNCIL_STATIONS:
            return None
        uprn = record.uprn.strip().lstrip("0")

        if (
            uprn
            in [
                "10093200695",  # WESTWOOD HOUSE, MELCHBOURNE ROAD, RISELEY, BEDFORD
                "200001852434",  # DEAN FARM, COLESDEN ROAD, COLMWORTH, BEDFORD
                "100080997913",  # CUCKOO BROOK HOUSE, ST. NEOTS ROAD, RENHOLD, BEDFORD
                "10002964874",  # HIGHFIELD HOUSE, GRAZE HILL LANE, RAVENSDEN, BEDFORD
                "100081214315",  # COWBRIDGE COTTAGE, AMPTHILL ROAD, KEMPSTON HARDWICK, BEDFORD
                "10090878428",  # THE GABLES, FALCON AVENUE, BEDFORD
                "100080013586",  # 50 FALCON AVENUE, BEDFORD
                "100080013584",  # 48 FALCON AVENUE, BEDFORD
                "100081209336",  # 140 CLAPHAM ROAD, CLAPHAM, BEDFORD
                "100081206809",  # TEMPLERS, 117A MIDLAND ROAD, BEDFORD
                "100080998897",  # SAILORS BRIDGE COTTAGE WOBURN ROAD, KEMPSTON
                "10090878776",  # WOLD FARM AIRFIELD ROAD, PODINGTON
                "10002972330",  # SUNCREST WESTFIELD ROAD, OAKLEY
                "10002975508",  # DUNGEE FARM, DUNGEE ROAD, ODELL, BEDFORD
                "100081209997",  # CLASSIC FURNITURE, 1A LONDON ROAD, BEDFORD
            ]
        ):
            return None

        if record.postcode in [
            # splits
            "MK43 9BD",
            # looks wrong
            "MK45 3JE",
        ]:
            return None
        return super().address_record_to_dict(record)
