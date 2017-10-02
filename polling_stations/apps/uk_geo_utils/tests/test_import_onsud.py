import os
from io import StringIO
from django.test import TestCase
from uk_geo_utils.models import Onsud
from uk_geo_utils.management.commands.import_onsud import Command


class OnsudImportTest(TestCase):

    def test_import_onsud(self):
        # check table is empty before we start
        self.assertEqual(0, Onsud.objects.count())

        # path to file we're going to import
        csv_path = os.path.abspath(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                '../fixtures/onsud'
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
        self.assertEqual(4, Onsud.objects.count())
