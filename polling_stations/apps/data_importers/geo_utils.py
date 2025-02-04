from django.contrib.gis.geos import LinearRing, MultiPolygon, Polygon
from django.db import transaction
from pollingstations.models import PollingDistrict
from polling_stations.db_routers import (
    get_principal_db_name,
    get_principal_db_connection,
)


def convert_linestring_to_multiploygon(linestring):
    points = linestring.coords

    # close the LineString so we can transform to LinearRing
    points = list(points)
    points.append(points[0])
    ring = LinearRing(points)

    # now we have a LinearRing we can make a Polygon.. and the rest is simple
    poly = Polygon(ring)
    return MultiPolygon(poly)


DB_NAME = get_principal_db_name()


@transaction.atomic(using=DB_NAME)
def fix_bad_polygons():
    # fix self-intersecting polygons
    print("running fixup SQL")
    table_name = PollingDistrict()._meta.db_table

    cursor = get_principal_db_connection().cursor()
    cursor.execute(
        """
        UPDATE {0}
        SET area=ST_Multi(ST_CollectionExtract(ST_MakeValid(area), 3))
        WHERE NOT ST_IsValid(area);
        """.format(table_name)
    )
