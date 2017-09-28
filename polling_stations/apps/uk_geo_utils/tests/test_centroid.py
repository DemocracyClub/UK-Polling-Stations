from django.test import TestCase
from uk_geo_utils.models import Address
from uk_geo_utils.helpers import centre_from_points_qs


class CentroidTest(TestCase):
    fixtures = ['test_centroid.json']

    def test_centroid_one_point(self):
        qs = Address.objects.filter(pk=1)
        centre = centre_from_points_qs(qs)
        self.assertEqual(
            "POINT (0.7208994610313337 52.0965737442737833)",
            centre.wkt
        )

    def test_centroid_two_points(self):
        qs = Address.objects.filter(pk__lte=2)
        centre = centre_from_points_qs(qs)

        self.assertEqual(
            "POINT (0.7217038959382571 52.0970394718411853)",
            centre.wkt
        )

        # SRID 4326 is a spherical geometry, so these won't be exact but
        # when we're dealing with points that are very close together like
        # this, they should be really really close to straight-line averages
        self.assertAlmostEqual(
            (0.7208994610313337 + 0.7225083308451804)/2,
            centre.x
        )
        self.assertAlmostEqual(
            (52.0965737442737833 + 52.0975051994085803)/2,
            centre.y
        )

    def test_centroid_three_points(self):
        qs = Address.objects.filter(pk__lte=3)
        centre = centre_from_points_qs(qs)
        self.assertEqual(
            "POINT (0.7195476867864934 52.0965233704130242)",
            centre.wkt
        )

    def test_centroid_poles(self):
        qs = Address.objects.filter(pk__gte=4)
        centre = centre_from_points_qs(qs)
        # centre point of the North and South pole
        # should be *somewhere* on the equator, right
        self.assertEqual(centre.y, 0)
