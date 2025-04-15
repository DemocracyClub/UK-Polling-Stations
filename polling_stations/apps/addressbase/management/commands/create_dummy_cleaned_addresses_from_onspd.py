import csv
from pathlib import Path

from django.core.management.base import BaseCommand
from django.db.models import F, Value, CharField, OuterRef, Subquery, Func
from django.db.models.functions import Concat, Replace

from addressbase.models import Address
from uk_geo_utils.models import Onspd


class AsEWKT(Func):
    """Calls the postgis ST_AsEWKT function to get strings like: SRID=4326;POINT(0.088849 51.43053)"""

    function = "ST_AsEWKT"
    output_field = CharField()


class Command(BaseCommand):
    help = (
        "Export postcodes that exist in ONSPD but not in AddressBase to a CSV file."
        "It's a good idea to name the output file according to the version of onspd it's derived from."
        "eg: python manage.py create_dummy_cleaned_addresses_from_onspd ONSPD_AUG_2024_addressbase_cleaned.csv"
    )

    def add_arguments(self, parser):
        parser.add_argument("output_file", type=str, help="Path to output CSV file")

    def handle(self, *args, **options):
        output_file = options["output_file"]

        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # First, create a queryset for postcodes that exist in the Address model
        existing_postcodes = Address.objects.filter(postcode=OuterRef("pcds")).values(
            "postcode"
        )

        # Main query
        results = (
            Onspd.objects.annotate(
                # Create "ONSPD:{postcode}" with whitespace removed
                uprn=Concat(
                    Value("ONSPD-", output_field=CharField()),
                    Replace("pcds", Value(" "), Value(""), output_field=CharField()),
                    output_field=CharField(),
                ),
                address=Value("", output_field=CharField()),
                postcode=F("pcds"),
                location_wkt=AsEWKT("location"),
                address_type=Value("", output_field=CharField()),
            )
            .filter(
                doterm="",  # Active postcodes (not terminated)
                usertype="0",  # Standard geographic postcodes
            )
            .exclude(
                # Exclude postcodes that exist in the Address model
                pk__in=Subquery(existing_postcodes)
            )
            .exclude(
                pcds__startswith="BT"  # Exclude postcodes in Northern Ireland
            )
            .exclude(
                pcds__startswith="GY"  # Exclude postcodes in Guernsey
            )
            .exclude(
                pcds__startswith="IM"  # Exclude postcodes in Isle of Man
            )
            .exclude(
                pcds__startswith="JE"  # Exclude postcodes in Jersey
            )
            .exclude(
                pcds__startswith="GIR"  # Exclude postcodes for banks
            )
        )

        # Write results to CSV without header
        with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)

            # Get all results as a list of tuples
            results_list = list(
                results.values_list(
                    "uprn", "address", "postcode", "address_type", "location_wkt"
                )
            )

            # Write all rows at once
            writer.writerows(results_list)

            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully exported {len(results_list)} records to {output_file}"
                )
            )
