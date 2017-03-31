from django.test import TestCase
from django.core.management import call_command

import vcr

from councils.models import Council
from councils.management.commands.import_councils import Command


class TestCouncilImporter(TestCase):

    @vcr.use_cassette(
    'fixtures/vcr_cassettes/test_get_contact_info_from_yvm.yaml')
    def test_get_contact_info_from_yvm(self):
        council_info = Command().get_contact_info_from_yvm('E07000044')
        assert council_info['name'] == 'South Hams District Council'
        assert council_info['website'].startswith('http://')

    @vcr.use_cassette(
        'fixtures/vcr_cassettes/test_import_councils.yaml')
    def test_import_councils(self):
        assert Council.objects.count() == 0
        with self.settings(
                MAPIT_URL="http://mapit.democracyclub.org.uk/",
                COUNCIL_TYPES=["LBO", ]):
            call_command('import_councils', '-n')
        assert Council.objects.count() == 33
