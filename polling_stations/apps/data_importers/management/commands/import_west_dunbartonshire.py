from addressbase.models import UprnToCouncil
from data_importers.management.commands import BaseHalarose2026UpdateCsvImporter


class Command(BaseHalarose2026UpdateCsvImporter):
    council_id = "WDU"
    addresses_name = "2026-05-07/2026-03-16T14:15:07.857416/combined.csv"
    stations_name = "2026-05-07/2026-03-16T14:15:07.857416/combined.csv"
    elections = ["2026-05-07"]

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
                self.COUNCIL_STATIONS.add(record.pollingvenueid)

    def address_record_to_dict(self, record):
        if record.pollingvenueid not in self.COUNCIL_STATIONS:
            return None
        uprn = record.uprn.strip().lstrip("0")

        if uprn in [
            "129048743",  # HIGHDYKES FARM, STIRLING ROAD, MILTON, DUMBARTON
        ]:
            return None

        if record.postcode in (
            # splits
            "G82 4JS",
            "G81 3PY",
            "G82 3LE",
        ):
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        if record.pollingvenueid not in self.COUNCIL_STATIONS:
            return None
        # address correction from council:
        # old: DALMUIR BARCLAY PARISH CHURCH, 21 DURBAN AVENUE, CLYDEBANK, G81 4JH
        # new: DALMUIR BARCLAY PARISH CHURCH, 20 DURBAN AVENUE, CLYDEBANK, G81 4JH
        if self.get_station_hash(record) in [
            "1-dalmuir-barclay-parish-church",
            "2-dalmuir-barclay-parish-church",
            "3-dalmuir-barclay-parish-church",
            "4-dalmuir-barclay-parish-church",
        ]:
            record = record._replace(pollingstationaddress1="20 DURBAIN AVENUE")

        return super().station_record_to_dict(record)
