from addressbase.models import UprnToCouncil
from data_finder.helpers import geocode_point_only, PostcodeError
from data_importers.management.commands import BaseHalaroseCsvImporter


class Command(BaseHalaroseCsvImporter):
    council_id = "WLN"
    addresses_name = (
        "2022-05-05/2022-03-09T09:56:54.102748/polling_station_export-2022-03-02 2.csv"
    )
    stations_name = (
        "2022-05-05/2022-03-09T09:56:54.102748/polling_station_export-2022-03-02 2.csv"
    )
    elections = ["2022-05-05"]

    def pre_import(self):
        # We need to consider rows that don't have a uprn when importing data.
        # However there are lots of rows for other councils in this file.
        # So build a list of stations from rows that do have UPRNS
        # and then use that list of stations to make sure we check relevant rows, even if they don't have a UPRN

        council_uprns = set(
            UprnToCouncil.objects.exclude(
                uprn="135047773"
            )  # because it's in West Lothian but votes in Edinburgh...
            .filter(lad=self.council.geography.gss)
            .values_list("uprn", flat=True)
        )
        self.COUNCIL_STATIONS = set()
        data = self.get_addresses()

        for record in data:
            if record.uprn in council_uprns:
                self.COUNCIL_STATIONS.add(self.get_station_hash(record))

    def address_record_to_dict(self, record):
        if self.get_station_hash(record) not in self.COUNCIL_STATIONS:
            return None

        if record.housepostcode in [
            "EH54 8FF",
            "EH48 3HL",
            "EH48 2UA",
            "EH48 2US",
            "EH55 8RR",
            "EH49 6BQ",
            "EH48 2GT",
            "EH47 7NL",
            "EH47 0EY",
            "EH53 0JR",
            "EH49 6BD",
        ]:
            return None

        return super().address_record_to_dict(record)

    def get_station_postcode(self, record):
        # postcode does not appear in a consistent column
        # return the contents of the last populated address
        # field and we'll attempt to geocode with that
        for field in [
            "pollingstationpostcode",
            "pollingstationaddress_3",
            "pollingstationaddress_2",
        ]:
            if getattr(record, field):
                if getattr(record, field).startswith("EH"):
                    return getattr(record, field).strip()

        return None

    def get_station_point(self, record):
        if not self.allow_station_point_from_postcode:
            return None

        location = None

        # geocode using postcode
        postcode = self.get_station_postcode(record)
        if postcode == "":
            return None

        try:
            location_data = geocode_point_only(postcode)
            location = location_data.centroid
        except PostcodeError:
            location = None

        return location

    def station_record_to_dict(self, record):
        if self.get_station_hash(record) not in self.COUNCIL_STATIONS:
            return None

        return super().station_record_to_dict(record)
