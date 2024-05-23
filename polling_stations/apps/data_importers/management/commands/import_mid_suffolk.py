from addressbase.models import UprnToCouncil
from data_importers.management.commands import BaseDemocracyCountsCsvImporter


class Command(BaseDemocracyCountsCsvImporter):
    council_id = "MSU"
    addresses_name = "2024-07-04/2024-05-24T13:28:32.606427/BMSDC PD Code data.csv"
    stations_name = (
        "2024-07-04/2024-05-24T13:28:32.606427/BMSDC Polling station data.csv"
    )
    elections = ["2024-07-04"]
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

        if record.uprn in [
            "10095541644",  # DOVEDALE, BROCKFORD ROAD, MENDLESHAM, STOWMARKET
            "200003810799",  # GABLES BARN, GOSBECK ROAD, HELMINGHAM, STOWMARKET
            "10094151033",  # GABLES BARN, GOSBECK ROAD, HELMINGHAM, STOWMARKET
            "10094151030",  # 10 SKIPPER CLOSE, THURSTON, BURY ST. EDMUNDS
            "200003806873",  # BADLEY COTTAGE, LITTLE LONDON, COMBS, STOWMARKET
        ]:
            return None

        if record.postcode in [
            # split
            "IP30 9NY",
            "IP14 5PE",
            "IP14 6ET",
            "IP14 5LN",
            # suspect
            "IP14 4FW",
            "IP31 3FL",
        ]:
            return None

        return super().address_record_to_dict(record)
