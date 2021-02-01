from django.core.management.base import BaseCommand
from django.db import connection
from pathlib import Path


class Command(BaseCommand):
    """
    This creates a lookup csv of uprn and council GSS codes.
    This can then be imported using 'import_uprn_council_lookup'.
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "-d", "--destination", help="Path to write csv to", default=None
        )

    def handle(self, *args, **kwargs):

        self.cursor = connection.cursor()
        # Set where we'll write the join query to.
        if kwargs["destination"]:
            self.dst = Path(kwargs["destination"]).open("w")
        else:
            self.dst = Path("./uprn-to-councils.csv").open("w")

        # Build the temporary subdivided council polygon table
        # See http://blog.cleverelephant.ca/2019/11/subdivide.html for why we're doing this.
        # tl;dr point in polygon lookups are super fast on small geometries.
        self.stdout.write("Creating subdivided councils table...")
        self.cursor.execute(
            """
            DROP TABLE IF EXISTS councils_council_subdivided;
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE councils_council_subdivided AS
            SELECT gss, st_subdivide(geography) AS geom
            FROM councils_councilgeography;
            """
        )

        # spatial join between councils_council_subdivided and addressbase
        # & dump out a CSV file
        self.stdout.write("Joining addresses to councils...")
        self.cursor.copy_expert(
            """
            COPY (SELECT
                    a.uprn as uprn,
                    c.gss as lad,
                    '' as polling_station_id
                FROM
                    addressbase_address a
                    JOIN
                    councils_council_subdivided c
                    ON
                    ST_Covers(c.geom, a.location)
                    )
                TO STDOUT

            with DELIMITER ',';
            """,
            self.dst,
        )
        self.stdout.write(f"Output written to: {self.dst.name}")

        # Drop councils_council_subdivided
        self.stdout.write("Dropping subdivided councils table...")
        self.cursor.execute(
            """
            DROP TABLE councils_council_subdivided;
            """
        )

        self.stdout.write(
            f"To import this data run: python manage.py import_uprn_council_lookup {self.dst.name}"
        )
