import csv
import tempfile
from pathlib import Path

from django.contrib.gis.geos import Point
from django.core.management import BaseCommand
from django.db import connection
from django.forms.models import model_to_dict

from addressbase.models import UprnToCouncil, Address
from councils.models import Council
from data_importers.base_importers import BaseStationsImporter, CsvMixin
from data_importers.data_types import StationSet, AddressList
from pollingstations.models import PollingStation, CustomFinder

ADDRESSES_FIELDS = ["uprn", "address", "postcode", "location", "addressbase_postal"]
UPRN_FIELDS = ["uprn", "lad", "polling_station_id", "advance_voting_station_id"]
STATION_FIELDS = [
    "internal_council_id",
    "address",
    "postcode",
    "location",
    "council_id",
]


class Command(BaseStationsImporter, CsvMixin):
    council_id = "EONI"
    council_gss_code = "EONI"
    stations_name = "eoni_stations.csv"
    stations_filetype = "csv"
    csv_encoding = "latin-1"

    def add_arguments(self, parser):
        parser.add_argument("eoni_csv", help="The path to the EONI export csv")
        parser.add_argument(
            "--stations-only",
            help="Don't process address, only update stations",
            action="store_true",
        )

    def handle(self, *args, **options):
        self.eoni_export_path = Path(options["eoni_csv"])
        self.eoni_data_root = self.eoni_export_path.absolute().parent
        self.addresses_path = self.eoni_data_root / "eoni_address.csv"
        self.uprn_to_council_path = self.eoni_data_root / "eoni_uprn_to_council.csv"
        self.stations_path = self.eoni_data_root / "eoni_stations.csv"
        self.stations_only = options.get("stations_only")
        self.pre_process_data()
        self.copy_data()
        self.council = self.add_pseudo_council()
        super().handle(*args, **options)

    def teardown(self, council):
        # Only remove old polling stations, as the UPRN to Council table
        # is populated by this command previously, so deleting data form it
        # isn't useful.
        CustomFinder.objects.filter(area_code="N07000001").delete()
        PollingStation.objects.filter(council=council).delete()

    def get_base_folder_path(self):
        return str(self.eoni_data_root)

    def pre_process_data(self):
        if not self.stations_only:
            addresses = csv.DictWriter(
                open(self.addresses_path, "w", encoding="latin-1"),
                fieldnames=ADDRESSES_FIELDS,
            )
            addresses.writeheader()
            uprns = csv.DictWriter(
                open(self.uprn_to_council_path, "w", encoding="latin-1"),
                fieldnames=UPRN_FIELDS,
            )
            uprns.writeheader()

        stations = csv.DictWriter(
            open(self.stations_path, "w", encoding="latin-1"),
            fieldnames=STATION_FIELDS,
        )
        stations.writeheader()
        station_data = {}

        with self.eoni_export_path.open("r", encoding="latin-1") as eoni_csv:
            # Do a single loop over the whole data file
            reader = csv.DictReader(eoni_csv)
            for row in reader:
                if not self.stations_only:
                    address_location = Point(
                        int(row["PRO_X_COR"]), int(row["PRO_Y_COR"]), srid=29902
                    )
                    address_location.transform(4326)
                    addresses.writerow(
                        {
                            "uprn": row["PRO_UPRN"].strip(),
                            "address": row["PRO_FULLADDRESS"].strip(),
                            "postcode": row["PRO_POSTCODE"].strip(),
                            "location": address_location.ewkt,
                            "addressbase_postal": "D",
                        }
                    )

                    uprns.writerow(
                        {
                            "uprn": row["PRO_UPRN"],
                            "lad": "EONI",
                            "polling_station_id": row["PREM_ID"],
                            "advance_voting_station_id": "NULL",
                        }
                    )

                station_data[row["PREM_ID"]] = {
                    "internal_council_id": row["PREM_ID"],
                    "postcode": row["PREM_POSTCODE"].strip(),
                    "address": row["PREM_FULLADDRESS"],
                    "location_y": row["PREM_Y_COR"],
                    "location_x": row["PREM_X_COR"],
                    "council_id": "EONI",
                }
            for internal_council_id, station in station_data.items():
                location = Point(
                    int(station.pop("location_x")),
                    int(station.pop("location_y")),
                    srid=29902,
                )
                location.transform(4326)
                station["location"] = location.ewkt
                stations.writerow(station)

    def copy_data(self):
        # Clear old data
        PollingStation.objects.filter(council_id="EONI").delete()

        if not self.stations_only:
            Address.objects.filter(uprntocouncil__lad="EONI").delete()
            UprnToCouncil.objects.filter(lad="EONI").delete()

            cursor = connection.cursor()
            cursor.copy_expert(
                "COPY addressbase_address FROM STDIN CSV HEADER",
                open(self.addresses_path),
            )
            cursor.copy_expert(
                "COPY addressbase_uprntocouncil FROM STDIN WITH NULL AS 'NULL' CSV HEADER",
                open(self.uprn_to_council_path),
            )

    def add_pseudo_council(self):
        """
        EONI isn't a real council, but people only need to contact EONI about
        elections, and never the local authority.

        Because of this, we create a fake council with EONI's contact details
        that we can link each NI address to.
        """
        random_ni_council = Council.objects.filter(
            identifiers__icontains="N09000"
        ).first()
        new_council_data = model_to_dict(random_ni_council)
        new_council_data.pop("users", None)
        new_council_data["council_id"] = "EONI"
        new_council_data["identifiers"] = ["EONI"]

        council, _ = Council.objects.update_or_create(
            council_id=new_council_data.pop("council_id"), defaults=new_council_data
        )
        return council

    def station_record_to_dict(self, record):
        return {
            "internal_council_id": getattr(record, "internal_council_id").strip(),
            "postcode": record.postcode,
            "address": record.address,
            "location": Point().from_ewkt(record.location),
        }

    def import_data(self):
        # We only need to import stations as addresses and UPRN to Council
        # is added using COPY
        self.stations = StationSet()
        self.import_polling_stations()
        self.stations.save()

    def check_in_council_bounds(self, station_record):
        if not station_record["postcode"].startswith("BT"):
            return False
        return True
