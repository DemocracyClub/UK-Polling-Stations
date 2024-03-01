from addressbase.models import UprnToCouncil
from data_importers.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "SOX"
    addresses_name = "2024-05-02/2024-03-01T17:07:17.279474/Democracy_Club__02May2024(Extracted 1 March 2024).tsv"
    stations_name = "2024-05-02/2024-03-01T17:07:17.279474/Democracy_Club__02May2024(Extracted 1 March 2024).tsv"
    elections = ["2024-05-02"]
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

        return super().station_record_to_dict(record)

    def address_record_to_dict(self, record):
        if record.polling_place_id not in self.COUNCIL_STATIONS:
            return None

        uprn = record.property_urn.strip().lstrip("0")

        if uprn in [
            "10033006434",  # GLADE HOUSE, PISHILL, HENLEY-ON-THAMES
        ]:
            return None

        if record.addressline6 in [
            # split
            "RG8 0PY",
            "OX11 7SE",
            "OX11 7TP",
            # suspect
            "OX44 7NW",
        ]:
            return None

        return super().address_record_to_dict(record)
