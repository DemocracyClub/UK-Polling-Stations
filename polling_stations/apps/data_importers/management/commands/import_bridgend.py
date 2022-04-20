from addressbase.models import UprnToCouncil
from core.opening_times import OpeningTimes
from data_importers.management.commands import BaseHalaroseCsvImporter
from data_importers.mixins import AdvanceVotingMixin
from pollingstations.models import AdvanceVotingStation, PollingStation


class Command(BaseHalaroseCsvImporter, AdvanceVotingMixin):
    council_id = "BGE"
    addresses_name = (
        "2022-05-05/2022-04-14T10:42:05.436399/polling_station_export-2022-04-14.csv"
    )
    stations_name = (
        "2022-05-05/2022-04-14T10:42:05.436399/polling_station_export-2022-04-14.csv"
    )
    elections = ["2022-05-05"]

    def address_record_to_dict(self, record):

        if record.housepostcode in [
            "CF31 1NP",
            "CF31 1PL",
            "CF31 5FD",
            "CF32 0NR",
            "CF32 8TY",
            "CF32 9YB",
            "CF33 4PT",
            "CF33 6PL",
            "CF34 0UF",
            "CF34 9SD",
            "CF35 6BN",
            "CF35 6GD",
            "CF35 6HZ",
            "CF35 6NA",
            "CF31 2DL",
        ]:
            return None

        return super().address_record_to_dict(record)

    def station_record_to_dict(self, record):
        # Pyle Rugby Football Club Brynglas Terrace Pyle Bridgend CF36 6AG
        if record.pollingstationnumber == "35":
            record = record._replace(pollingstationpostcode="CF33 6AG")

        return super().station_record_to_dict(record)

    def add_advance_voting_stations(self):
        opening_times = OpeningTimes()
        opening_times.add_open_time("2022-05-03", "07:00", "21:00")
        opening_times.add_open_time("2022-05-04", "07:00", "21:00")

        advance_station_ids = (
            "1-portacabin-at-hunters-lodge",
            "2-the-williams-memorial-hall",
            "3-hunters-lodge",
            "4-portacabin-at-arosfa",
            "5-brackla-community-centre",
            "6-brackla-community-centre",
            "24-cornelly-community-centre",
            "25-cornelly-community-centre",
            "26-cornelly-changing-rooms",
            "35-pyle-rugby-football-club",
            "36-pyle-life-centre",
            "37-talbot-community-centre",
            "38-cefn-cribwr-comm-centre",
            "71-bryncethin-community-centre",
            "72-st-brides-minor-memorial-hall",
            "73-sarn-and-bryncethin-community-centre",
            "74-sarn-and-bryncethin-community-centre",
            "75-fox-hounds",
            "76-wesley-church-centre-tondu",
            "77-ynysawdre-parish-hall",
        )
        for station_id in advance_station_ids:
            station = PollingStation.objects.get(
                internal_council_id=station_id, council_id=self.council_id
            )
            advance_station = AdvanceVotingStation(
                name=station.address.split("\n")[0],
                address="\n".join(station.address.split("\n")[1:]),
                postcode="NP23 6GL",
                location=station.location,
                opening_times=opening_times.as_string_table(),
            )
            advance_station.save()
            UprnToCouncil.objects.filter(
                lad=self.council.geography.gss,
                polling_station_id=station.internal_council_id,
            ).update(advance_voting_station=advance_station)
