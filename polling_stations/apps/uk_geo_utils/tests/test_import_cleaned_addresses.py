import os
from io import StringIO
from django.test import TestCase, override_settings
from uk_geo_utils.models import Address
from uk_geo_utils.management.commands.import_cleaned_addresses import Command


# TODO: This override can be removed when you spin this
# out into a seperate package. It is only needed because
# we're running the tests inside WhereDIV as a host app
@override_settings(ADDRESS_MODEL='uk_geo_utils.Address')
class CleanedAddressImportTest(TestCase):

    def test_import_onsud(self):
        # check table is empty before we start
        self.assertEqual(0, Address.objects.count())

        # path to file we're going to import
        csv_path = os.path.abspath(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                '../fixtures/cleaned_addresses'
            )
        )

        cmd = Command()

        # supress output
        out = StringIO()
        cmd.stdout = out

        # import data
        opts = {
            'cleaned_ab_path': csv_path,
        }
        cmd.handle(**opts)

        # ensure all our tasty data has been imported
        self.assertEqual(4, Address.objects.count())
