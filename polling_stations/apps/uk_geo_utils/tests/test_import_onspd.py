import os
from io import StringIO
from django.contrib.gis.geos import Point
from django.test import TestCase
from uk_geo_utils.models import Onspd
from uk_geo_utils.management.commands.import_onspd import Command


class OnsudImportTest(TestCase):

    def test_import_onspd(self):
        # check table is empty before we start
        self.assertEqual(0, Onspd.objects.count())

        # path to file we're going to import
        csv_path = os.path.abspath(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                '../fixtures/onspd'
            )
        )

        cmd = Command()

        # supress output
        out = StringIO()
        cmd.stdout = out

        # import data
        opts = {
            'path': csv_path,
        }
        cmd.handle(**opts)

        # ensure all our tasty data has been imported
        self.assertEqual(4, Onspd.objects.count())

        # row with valid grid ref should have valid Point() location
        al11aa = Onspd.objects.filter(pcds="AL1 1AA")[0]
        self.assertEqual(Point(-0.341337, 51.749084, srid=4326), al11aa.location)

        # row with invalid grid ref should have NULL location
        im11aa = Onspd.objects.filter(pcds="IM1 1AA")[0]
        self.assertIsNone(im11aa.location)
