from itertools import chain
from pathlib import Path

import psycopg2.extras
from django.contrib.gis.gdal import DataSource, OGRGeomType
from django.contrib.gis.geos import MultiPolygon, Polygon
from django.core.management.base import BaseCommand
from django.db import connection


class LayerValidationError(Exception):
    def __init__(self, msg):
        self.msg = msg


class Command(BaseCommand):
    """
    Takes a polygon layer (or layers) and returns the result of a point in polygon
    spatial join between addressbase and the layer(s) as a csv (or csvs).

    example usage:
     ./manage.py create_addressbase_lookup --shard-on-outcode --cleanup --destination parl2023-lookup  parl2023/constituencies.gpkg
    """

    def __init__(self):
        self.datasource = None
        self.tables = []
        self.subdivided_tables = []
        self.layer_names = []
        self.datasource_name = None
        self.dst_dir = Path.cwd()
        self.shard_on_outcode = False
        super().__init__()

    def add_arguments(self, parser):
        parser.add_argument(
            "datasource",
            help="The path to the polygon datasource - should be a gdal readable file",
        )
        parser.add_argument(
            "-d",
            "--destination",
            help="Path of directory to write csv to",
            default=None,
        )
        parser.add_argument(
            "-c",
            "--cleanup",
            action="store_true",
            help="Delete tables used to create lookups",
        )
        parser.add_argument(
            "-s",
            "--shard-on-outcode",
            action="store_true",
            help="Create one file per outcode, much slower",  # TODO add multithreading
        )

    def layer_path_name(self, layer):
        return f"{self.datasource}|layername={layer}"

    def cleanup(self):
        self.stdout.write("cleaning up...")
        with connection.cursor() as cursor:
            for table in self.tables + self.subdivided_tables:
                self.stdout.write(f"Dropping table {table}")
                cursor.execute(f"DROP TABLE IF EXISTS {table};")

    def get_ewkt_multipolygon_from_gdal_geom(self, feature, layer):
        if isinstance(feature.geom.geos, MultiPolygon):
            return feature.geom.geos.ewkt
        if isinstance(feature.geom.geos, Polygon):
            return MultiPolygon(feature.geom.geos).ewkt

        raise TypeError(
            f"Expected Polygon or MultiPolygon from feature {feature.fid} in {self.layer_path_name(layer)}"
        )

    def check_fields(self, layer):
        for field_name in ["official_identifier", "name"]:
            if field_name not in layer.fields:
                raise LayerValidationError(
                    f"""Field called '{field_name}' missing from {self.layer_path_name(layer)}.
                        Found following fields: {layer.fields}
                    """
                )

    def check_geom_type(self, layer):
        valid_geom_types = (OGRGeomType("Polygon"), OGRGeomType("MultiPolygon"))
        if layer.geom_type not in valid_geom_types:
            raise LayerValidationError(
                f"""Layer must have geom_type in {[gt.name for gt in  valid_geom_types]}.
                {self.layer_path_name(layer)} has geom_type of {layer.geom_type.name}
                """
            )

    def check_srs(self, layer):
        if layer.srs.srid != 4326:
            srs = layer.srs
            raise LayerValidationError(
                f"""Layer must be in SRS WGS 84 (EPSG:4326)
                {self.layer_path_name(layer)} is in {srs.name} ({srs["AUTHORITY"]}:{srs.srid})
                """
            )

    def validate_datasource(self):
        for layer in self.datasource:
            self.stdout.write(
                f"Running validation checks for {self.layer_path_name(layer)}"
            )
            self.check_fields(layer)
            self.check_geom_type(layer)
            self.check_srs(layer)

    def create_table(self, layer, table_name):
        with connection.cursor() as cursor:
            self.stdout.write(f"Creating table {table_name} to store {layer}")
            cursor.execute(
                f"""
                DROP TABLE IF EXISTS {table_name};
                CREATE UNLOGGED TABLE {table_name} (
                  official_identifier TEXT,
                  name TEXT,
                  geom geometry(MultiPolygon, 4326)
                );
                """
            )
            self.tables.append(table_name)

    def create_subdivided_table(self, table_to_subdivide, table_name):
        with connection.cursor() as cursor:
            self.stdout.write(
                f"Creating table {table_to_subdivide} by subdividing geoms in {table_name}"
            )
            cursor.execute(
                f"""
                DROP TABLE IF EXISTS {table_name};
                CREATE UNLOGGED TABLE {table_name} AS
                SELECT official_identifier, name, st_subdivide(geom) as geom
                FROM {table_to_subdivide}
                """
            )
            self.subdivided_tables.append(table_name)
            self.stdout.write(f"Creating gidx_{table_name} on (geom) in {table_name}")
            cursor.execute(
                f"CREATE INDEX gidx_{table_name} on {table_name} USING gist (geom);"
            )

    def copy_data(self, layer):
        # Inspired by https://hakibenita.com/fast-load-data-python-postgresql
        iter_features = (
            {
                "official_identifier": feature.get("official_identifier"),
                "name": feature.get("name"),
                "geom": self.get_ewkt_multipolygon_from_gdal_geom(feature, layer),
            }
            for feature in layer
        )
        with connection.cursor() as cursor:
            self.stdout.write(f"importing from {layer} to cal_{layer}")
            psycopg2.extras.execute_batch(
                cursor,
                f"""
                INSERT INTO cal_{layer} (official_identifier, name, geom) VALUES (
                    %(official_identifier)s,
                    %(name)s,
                    ST_GeomFromEWKT(%(geom)s)
                )
                """,
                iter_features,
            )

    def load_layer(
        self,
        layer,
    ):
        self.create_table(layer, f"cal_{layer}")
        self.copy_data(layer)
        self.create_subdivided_table(f"cal_{layer}", f"cal_{layer}_subdivided")

    def single_lookup_query_string(self):
        layer_selects = [
            (
                f"\n{ln}.official_identifier as {ln}_official_identifier,\n{ln}.name as {ln}_name"
            )
            for ln in self.layer_names
        ]
        layer_joins = [
            f"\nJOIN cal_{ln}_subdivided {ln} ON ST_Covers({ln}.geom, a.location)"
            for ln in self.layer_names
        ]

        newline = "\n"
        newline_comma = "\n,"
        return f"""
                SELECT
                    a.uprn as uprn,
                    a.address as address,
                    a.postcode as postcode,
                    split_part(a.postcode, ' ',1) as outcode,
                    {newline_comma.join(layer_selects)}
                FROM
                    addressbase_address a
                    {newline.join(layer_joins)}
                """

    @property
    def single_lookup_dst_path(self):
        return self.dst_dir / f"addressbase_to_{self.datasource_name}_lookup.csv"

    def create_single_lookup(self):
        destination_path = self.single_lookup_dst_path
        query_string = self.single_lookup_query_string()
        with connection.cursor() as cursor:
            self.stdout.write(f"creating lookup {destination_path.name}...")
            with destination_path.open("w") as destination:
                cursor.copy_expert(
                    f"""
                    COPY ({query_string})
                    TO STDOUT
                    WITH (FORMAT 'csv', HEADER);
                    """,
                    destination,
                )
        self.stdout.write(f"Output written to: {destination_path}")

    def create_outcode_lookup(self, outcode, cursor):
        destination_path = self.dst_dir / "outcodes" / f"{outcode.strip()}.csv"
        query_string = (
            f"{self.single_lookup_query_string()} WHERE a.postcode LIKE '{outcode}%'"
        )

        self.stdout.write(f"creating lookup {destination_path.name}...")
        with destination_path.open("w") as destination:
            cursor.copy_expert(
                f"""
                COPY ({query_string})
                TO STDOUT
                WITH (FORMAT 'csv', HEADER);
                """,
                destination,
            )
        self.stdout.write(f"Output written to: {destination_path}")

    def create_sharded_lookup(self):
        (self.dst_dir / "outcodes").mkdir(exist_ok=True, parents=True)
        outcodes = self.get_outcodes()
        with connection.cursor() as cursor:
            for outcode in outcodes:
                self.create_outcode_lookup(outcode, cursor)

    def get_outcodes(self):
        with connection.cursor() as cursor:
            cursor.execute(
                "Select distinct split_part(a.postcode, ' ',1) as outcode from addressbase_address a"
            )
            return [f"{outcode} " for outcode in chain.from_iterable(cursor.fetchall())]

    def create_lookup(self):
        if self.shard_on_outcode:
            self.create_sharded_lookup()
        else:
            self.create_single_lookup()

    def create_parquet_files(self):
        try:
            # We only need polars for this script, so don't force it on everyone
            # Just pip install if you want parquets.
            import polars as pl
        except ModuleNotFoundError:
            self.stdout.write("Polars not installed. Not writing parquet files.")
            pass

        def write_parquet(csv_path: Path, parquet_path: Path):
            df = pl.read_csv(csv_path)
            df.write_parquet(parquet_path, compression="snappy")

        if not self.shard_on_outcode:
            write_parquet(
                self.single_lookup_dst_path,
                self.single_lookup_dst_path.with_suffix(".parquet"),
            )

        if self.shard_on_outcode:
            parquet_dir = self.dst_dir / "parquet"
            parquet_dir.mkdir(parents=True, exist_ok=True)
            for csv_path in (self.dst_dir / "outcodes").glob("*.csv"):
                outcode = csv_path.stem
                write_parquet(csv_path, parquet_dir / f"{outcode}.parquet")

    def handle(self, *args, **kwargs):
        # Set polygon layer
        self.datasource = DataSource(kwargs["datasource"])
        self.validate_datasource()

        # Keep track of what we make, so we can clean up
        # and know what to tables to join on.
        self.tables = []
        self.subdivided_tables = []

        self.layer_names = [layer.name for layer in self.datasource]
        self.datasource_name = Path(kwargs["datasource"]).stem

        # Set where we'll write the csvs to.
        if kwargs["destination"]:
            self.dst_dir = Path(kwargs["destination"])
        else:
            self.dst_dir = Path.cwd()

        self.shard_on_outcode = kwargs["shard_on_outcode"]

        for layer in self.datasource:
            self.load_layer(layer)

        self.create_lookup()

        self.create_parquet_files()

        if kwargs["cleanup"]:
            self.cleanup()
