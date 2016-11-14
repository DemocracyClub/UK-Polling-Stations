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
