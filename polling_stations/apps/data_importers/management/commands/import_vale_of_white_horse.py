from addressbase.models import UprnToCouncil
from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "VAL"
    addresses_name = "2024-07-04/2024-06-10T18:04:35.848427/SOXandVAL_combined.tsv"
    stations_name = "2024-07-04/2024-06-10T18:04:35.848427/SOXandVAL_combined.tsv"
    elections = ["2024-07-04"]
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

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.polling_place_id not in self.COUNCIL_STATIONS:
            return None

        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10014028754",  # CHURCH PATH FARM, FARINGDON
        ]:
            return None

        if record.addressline6 in [
            # split
            "OX13 5ND",
            "OX13 5GW",
            "SN7 8DJ",
        ]:
            return None

        return super().address_record_to_dict(record)
