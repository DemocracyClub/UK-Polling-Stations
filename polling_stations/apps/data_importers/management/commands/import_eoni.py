import csv
import datetime
from pathlib import Path
from typing import Dict, Any

from addressbase.models import Address, UprnToCouncil
from core.slack_client import SlackClient
from councils.models import Council
from data_importers.base_importers import BaseStationsImporter, CsvMixin
from data_importers.data_types import StationSet
from data_importers.event_helpers import record_teardown_event
from data_importers.event_types import DataEventType
from data_importers.models import DataEvent
from django.contrib.gis.geos import Point
from django.db import connections, transaction
from django.db.models import Q
from pollingstations.models import CustomFinder, PollingStation

from polling_stations.db_routers import get_principal_db_name
from polling_stations.settings.constants.councils import NIR_IDS

ADDRESSES_FIELDS = ["uprn", "address", "postcode", "location", "addressbase_postal"]
UPRN_FIELDS = ["uprn", "lad", "polling_station_id", "advance_voting_station_id"]
STATION_FIELDS = [
    "internal_council_id",
    "address",
    "postcode",
    "location",
    "council_id",
    "sample_uprn",
]

UPRN_TO_COUNCIL_CACHE = {}

DB_NAME = get_principal_db_name()


class Command(BaseStationsImporter, CsvMixin):
    council_id = "ANN"  # This is a hack to make the command initialise
    stations_name = "eoni_stations.csv"
    stations_filetype = "csv"
    csv_encoding = "utf-8"
    eoni_csv_encoding = "latin-1"
    additional_report_councils = NIR_IDS
    elections = ["2024-07-04"]
    address_counts = {council_id: 0 for council_id in NIR_IDS}
    deduced_addresses = {}
    removed_addresses = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slack_client = None
        self.should_post_to_slack = False

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument("eoni_csv", help="The path to the EONI export csv")
        parser.add_argument(
            "--stations-only",
            help="Don't process address, only update stations",
            action="store_true",
        )
        parser.add_argument(
            "--cleanup", help="Delete intermediate CSVs", action="store_true"
        )
        parser.add_argument(
            "--reprojected",
            help="Coordinates available in 4326. Fieldnames: PRO_{X,Y}_4326 & PREM_{X,Y}_4326",
            action="store_true",
        )
        parser.add_argument(
            "--slack",
            help="Post a report to slack in the channel specified",
            action="store",
        )

    def handle(self, *args, **options):
        if slack_channel := options.get("slack"):
            self.slack_client = SlackClient(channel=slack_channel)
            self.should_post_to_slack = True

        try:
            self.eoni_export_path = Path(options["eoni_csv"])
            self.eoni_data_root = self.eoni_export_path.absolute().parent

            self.paths = {
                "addresses": self.eoni_data_root / "eoni_address.csv",
                "uprn_to_council": self.eoni_data_root / "eoni_uprn_to_council.csv",
                "stations": self.eoni_data_root / "eoni_stations.csv",
            }
            self.stations_only = options.get("stations_only")
            self.pre_process_data(reprojected=options["reprojected"])
            self.clear_old_data()
            self.copy_data()
            self.assign_uprn_to_councils()
            super().handle(*args, **options)
            if options.get("cleanup"):
                [path.unlink() for path in self.paths.values() if path.exists()]

        except Exception as e:
            if self.should_post_to_slack:
                self.post_failure_to_slack(e)
            raise e

        else:
            if self.should_post_to_slack:
                self.post_to_slack()

    def record_import_event(self):
        election_dates = []
        if hasattr(self, "elections"):
            election_dates = [
                datetime.datetime.strptime(date_string, "%Y-%m-%d")
                for date_string in self.elections
            ]
        for council_id in NIR_IDS:
            DataEvent.objects.using(DB_NAME).create(
                council=self.get_council(council_id),
                upload=self.get_upload(),
                event_type=DataEventType.IMPORT,
                election_dates=election_dates,
            )

    def get_upload(self):
        return None

    def teardown(self, council):
        # Only remove old polling stations, as the UPRN to Council table
        # is populated by this command previously, so deleting data form it
        # isn't useful.
        with transaction.atomic():
            CustomFinder.objects.using(DB_NAME).filter(area_code="N07000001").delete()
            PollingStation.objects.using(DB_NAME).filter(
                council_id__in=NIR_IDS
            ).delete()
            for council_id in NIR_IDS:
                record_teardown_event(council_id)

    def get_base_folder_path(self):
        return str(self.eoni_data_root)

    def address_from_row(self, row, reprojected):
        if reprojected:
            address_location_ewkt = (
                f"SRID=4326;POINT({row['PRO_X_4326']} {row['PRO_Y_4326']})"
            )
        else:
            address_location = Point(
                int(row["PRO_X_COR"]), int(row["PRO_Y_COR"]), srid=29902
            )
            address_location.transform(4326)
            address_location_ewkt = address_location.ewkt

        postcode = row["PRO_POSTCODE"].strip()
        address = row["PRO_FULLADDRESS"].strip()
        if address.endswith(f", {postcode}"):
            address = address.replace(f", {postcode}", "")
        return {
            "uprn": row["PRO_UPRN"].strip(),
            "address": address,
            "postcode": postcode,
            "location": address_location_ewkt,
            "addressbase_postal": "D",
        }

    def station_from_row(self, row, reprojected):
        if reprojected:
            station_location_ewkt = (
                f"SRID=4326;POINT({row['PREM_X_4326']} {row['PREM_Y_4326']})"
            )
        else:
            location = Point(
                int(row["PREM_X_COR"]),
                int(row["PREM_Y_COR"]),
                srid=29902,
            )
            location.transform(4326)
            station_location_ewkt = location.ewkt

        return {
            "internal_council_id": row["PREM_ID"],
            "postcode": row["PREM_POSTCODE"].strip(),
            "address": f'{row["PREM_NAME"].strip()}, {row["PREM_FULLADDRESS"].strip()}',
            "location": station_location_ewkt,
            "council_id": "EONI",
            "sample_uprn": row["PRO_UPRN"].strip(),
        }

    def uprn_from_row(self, row):
        return {
            "uprn": row["PRO_UPRN"],
            "lad": "EONI",
            "polling_station_id": row["PREM_ID"],
            "advance_voting_station_id": "NULL",
        }

    def pre_process_data(self, reprojected=False):
        station_data = {}
        address_data = []
        uprn_data = []

        with self.eoni_export_path.open(
            "r", encoding=self.eoni_csv_encoding
        ) as eoni_csv:
            # Do a single loop over the whole data file
            reader = csv.DictReader(eoni_csv)
            for row in reader:
                if not self.stations_only:
                    address_data.append(self.address_from_row(row, reprojected))
                    uprn_data.append(self.uprn_from_row(row))

                if row["PREM_ID"] not in station_data:
                    station_data[row["PREM_ID"]] = self.station_from_row(
                        row, reprojected
                    )
        self.write_csv(self.paths["stations"], STATION_FIELDS, station_data.values())
        if not self.stations_only:
            self.write_csv(self.paths["addresses"], ADDRESSES_FIELDS, address_data)
            self.write_csv(self.paths["uprn_to_council"], UPRN_FIELDS, uprn_data)

    def write_csv(self, path, fieldnames, data):
        with open(path, "w", encoding=self.csv_encoding) as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

    def clear_old_data(self):
        # Polling stations use reg codes
        PollingStation.objects.using(DB_NAME).filter(council_id__in=NIR_IDS).delete()

        if not self.stations_only:
            # UprnToCouncil uses GSS codes
            nir_and_eoni = [
                c.geography.gss
                for c in Council.objects.using(DB_NAME)
                .filter(council_id__in=NIR_IDS)
                .select_related("geography")
            ]
            nir_and_eoni.append("EONI")  # Include fake 'EONI' gss just in case
            Address.objects.using(DB_NAME).filter(
                uprntocouncil__lad__in=nir_and_eoni
            ).delete()
            UprnToCouncil.objects.using(DB_NAME).filter(lad__in=nir_and_eoni).delete()

    def copy_data(self):
        if not self.stations_only:
            cursor = connections[DB_NAME].cursor()
            with open(self.paths["addresses"]) as file:
                cursor.copy_expert(
                    "COPY addressbase_address FROM STDIN CSV HEADER",
                    file,
                )
            with open(self.paths["uprn_to_council"]) as file:
                cursor.copy_expert(
                    "COPY addressbase_uprntocouncil FROM STDIN WITH NULL AS 'NULL' CSV HEADER",
                    file,
                )

    def assign_uprn_to_councils(self):
        ni_councils = (
            Council.objects.using(DB_NAME)
            .filter(council_id__in=NIR_IDS)
            .select_related("geography")
        )
        for council in ni_councils:
            uprns_in_council = (
                UprnToCouncil.objects.using(DB_NAME)
                .filter(lad="EONI")
                .filter(uprn__location__within=council.geography.geography)
            )
            address_count = uprns_in_council.using(DB_NAME).update(
                lad=council.geography.gss
            )
            self.address_counts[council.council_id] = address_count

        self.assign_or_remove_left_over_addresses()

    def assign_or_remove_left_over_addresses(self):
        for address in Address.objects.using(DB_NAME).filter(uprntocouncil__lad="EONI"):
            others_in_postcode = (
                Address.objects.using(DB_NAME)
                .filter(postcode=address.postcode)
                .exclude(Q(Q(uprntocouncil__lad="EONI") | Q(uprn=address.uprn)))
                .distinct("uprntocouncil__lad")
            )
            if len(others_in_postcode) == 1:
                other_address = others_in_postcode[0]
                other_uprn = other_address.uprntocouncil
                other_uprn.refresh_from_db(using=DB_NAME)
                self.stdout.write(
                    f"Updating UprnToCouncil record for {address.uprn} with gss {other_uprn.lad}"
                )
                address_uprn = address.uprntocouncil
                address_uprn.lad = other_uprn.lad
                address_uprn.save(using=DB_NAME)
                self.deduced_addresses[address.uprn] = other_uprn.lad

            else:
                self.stdout.write(f"Council ambiguous for {address.uprn}, deleting")
                address.uprntocouncil.delete(using=DB_NAME)
                address.delete(using=DB_NAME)
                self.removed_addresses += 1

    def station_record_to_dict(self, record):
        if record.sample_uprn not in UPRN_TO_COUNCIL_CACHE:
            UPRN_TO_COUNCIL_CACHE[record.sample_uprn] = Council.objects.using(
                DB_NAME
            ).get(
                identifiers__contains=[
                    UprnToCouncil.objects.using(DB_NAME)
                    .get(uprn=record.sample_uprn)
                    .lad
                ]
            )
        station_council = UPRN_TO_COUNCIL_CACHE[record.sample_uprn]
        if station_council == self.council:
            return {
                "internal_council_id": getattr(record, "internal_council_id").strip(),
                "postcode": record.postcode,
                "address": record.address,
                "location": Point().from_ewkt(record.location),
            }
        return None

    def import_data(self):
        # We only need to import stations as addresses and UPRN to Council
        # is added using COPY
        ni_councils = Council.objects.using(DB_NAME).filter(council_id__in=NIR_IDS)
        for council in ni_councils:
            self.council = council
            self.council_id = council.council_id
            self.stations = StationSet()
            self.import_polling_stations()
            self.stations.save()

    def check_in_council_bounds(self, station_record):
        if not station_record["postcode"].startswith("BT"):
            return False
        return True

    def post_failure_to_slack(self, exception: Exception) -> None:
        try:
            response = self.slack_client.send_message(
                message=":warning: *EONI Data Import Failed*",
            )
            self.slack_client.send_message(
                message=f"Error: {str(exception)}", thread_ts=response.get("ts")
            )
        except Exception as slack_e:
            self.stderr.write(f"Error posting to Slack: {str(slack_e)}")

    def post_to_slack(self) -> None:
        try:
            response = self.post_header()
            thread_ts = response.get("ts")
            self.post_details(thread_ts)
        except Exception as e:
            self.stderr.write(f"Error posting to Slack: {str(e)}")

    def post_header(self) -> Dict[str, Any]:
        return self.slack_client.send_message(
            message=":house_buildings: *EONI Data Imported*",
        )

    def post_details(self, thread_ts: str) -> None:
        # Post address counts
        address_counts_text = ["*Address Counts by Council:*"]
        for council_id, count in self.address_counts.items():
            address_counts_text.append(f"- {council_id}: {count:,} addresses")

        self.slack_client.send_message(
            message="\n".join(address_counts_text),
            thread_ts=thread_ts,
        )

        # Post deduced addresses info if any
        if self.deduced_addresses:
            self.slack_client.send_message(
                message="\n".join(
                    f"Council inferred from other addresses in the same postcode for  {len(self.deduced_addresses):,} addresses.*"
                ),
                thread_ts=thread_ts,
            )

        # Post removed addresses info if any
        if self.removed_addresses:
            self.slack_client.send_message(
                message="\n".join(
                    f"Council ambiguous for  {len(self.deduced_addresses):,} addresses, so they've been discarded."
                ),
                thread_ts=thread_ts,
            )
