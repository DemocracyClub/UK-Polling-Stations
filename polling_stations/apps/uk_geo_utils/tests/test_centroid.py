from django.test import TestCase
from uk_geo_utils.models import Address
from uk_geo_utils.helpers import centre_from_points_qs


class CentroidTest(TestCase):
    fixtures = ['test_centroid.json']

    def test_centre_from_points_qs(self):
        qs = Address.objects.all()
        centre = centre_from_points_qs(qs)
        self.assertEqual(
            centre.wkt,
            "POINT (0.7195476867864934 52.0965233704130242)"
        )
