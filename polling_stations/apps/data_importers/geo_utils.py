from django.contrib.gis.geos import LinearRing, MultiPolygon, Polygon
from django.db import connection, transaction
from pollingstations.models import PollingDistrict


def convert_linestring_to_multiploygon(linestring):
    points = linestring.coords

    # close the LineString so we can transform to LinearRing
    points = list(points)
    points.append(points[0])
    ring = LinearRing(points)

    # now we have a LinearRing we can make a Polygon.. and the rest is simple
    poly = Polygon(ring)
    return MultiPolygon(poly)


@transaction.atomic
def fix_bad_polygons():
    # fix self-intersecting polygons
    print("running fixup SQL")
    table_name = PollingDistrict()._meta.db_table

    cursor = connection.cursor()
    cursor.execute(
        """
        UPDATE {0}
        SET area=ST_Multi(ST_CollectionExtract(ST_MakeValid(area), 3))
        WHERE NOT ST_IsValid(area);
        """.format(table_name)
    )
