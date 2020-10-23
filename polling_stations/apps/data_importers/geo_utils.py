from django.db import transaction
from django.db import connection
from pollingstations.models import PollingDistrict
from django.contrib.gis.geos import MultiPolygon, Polygon, LinearRing


def convert_linestring_to_multiploygon(linestring):
    points = linestring.coords

    # close the LineString so we can transform to LinearRing
    points = list(points)
    points.append(points[0])
    ring = LinearRing(points)

    # now we have a LinearRing we can make a Polygon.. and the rest is simple
    poly = Polygon(ring)
    multipoly = MultiPolygon(poly)
    return multipoly


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
        """.format(
            table_name
        )
    )
