from addressbase.models import UprnToCouncil
from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "MSU"
    addresses_name = (
        "2024-05-02/2024-02-27T18:06:31.069614/BMSDC Polling Districts extract.csv"
    )
    stations_name = (
        "2024-05-02/2024-02-27T18:06:31.069614/BMSDC Polling Station extract.csv"
    )
    elections = ["2024-05-02"]
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

    def station_record_to_dict(self, record):
        if record.stationcode not in self.COUNCIL_STATIONS:
            return None

        # All Saints Church Beyton, Church Road, Beyton, Bury Saint Edmunds IP30 9AL
        if record.stationcode == "M94":
            record = record._replace(xordinate="593395")
            record = record._replace(yordinate="262775")

        # Wetheringsett Village Hall, Church Street, Wetheringsett IP14 5PJ
        if record.stationcode == "M56":
            record = record._replace(xordinate="612591")
            record = record._replace(yordinate="266691")

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.stationcode not in self.COUNCIL_STATIONS:
            return None

        if record.uprn in [
            "10095541644",  # DOVEDALE, BROCKFORD ROAD, MENDLESHAM, STOWMARKET
            "200003810799",  # GABLES BARN, GOSBECK ROAD, HELMINGHAM, STOWMARKET
            "10094151033",  # GABLES BARN, GOSBECK ROAD, HELMINGHAM, STOWMARKET
            "10094151030",  # 10 SKIPPER CLOSE, THURSTON, BURY ST. EDMUNDS
        ]:
            return None

        if record.postcode in [
            # split
            "IP14 5LN",
            "IP14 5PE",
            "IP14 6ET",
            # suspect
            "IP14 4FW",
            "IP31 3FL",
        ]:
            return None

        return super().address_record_to_dict(record)
