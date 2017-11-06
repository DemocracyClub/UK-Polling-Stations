from io import StringIO

from django.test import TestCase
from django.conf import settings
from django.core.management import call_command

import vcr

from councils.models import Council
from councils.management.commands.import_councils import Command


class MockCouncilsImporter(Command):

    def get_json(self, url):
        auths = [
            { 'code': "E09000001", 'name': "City of London Corporation" },
            { 'code': "E09000002", 'name': "London Borough of Barking and Dagenham" },
            { 'code': "E09000003", 'name': "London Borough of Barnet" },
            { 'code': "E09000004", 'name': "London Borough of Bexley" },
            { 'code': "E09000005", 'name': "London Borough of Brent" },
            { 'code': "E09000006", 'name': "London Borough of Bromley" }
        ]
        if url == settings.GB_BOUNDARIES_URL:
            out = []
            for auth in auths:
                out.append({
                    "type": "Feature",
                    "properties": {
                        "objectid": 1,
                        "lad16cd": auth['code'],
                        "lad16nm": auth['name'],
                        "lad14nmw": " ",
                        "st_areashape": 123,
                        "st_lengthshape": 4564
                    },
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [-0.354931354522705, 51.462162607847056],
                            [-0.3518199920654297, 51.462162607847056],
                            [-0.354931354522705, 51.46355294206526],
                            [-0.354931354522705, 51.462162607847056]
                        ]]
                    }
                })
            return {'features': out}
        if url == settings.NI_BOUNDARIES_URL:
            return {'features': []}


class TestCouncilImporter(TestCase):

    @vcr.use_cassette(
    'fixtures/vcr_cassettes/test_get_contact_info_from_yvm.yaml')
    def test_get_contact_info_from_yvm(self):
        council_info = Command().get_contact_info_from_yvm('E07000044')
        assert council_info['name'] == 'South Hams District Council'
        assert council_info['website'].startswith('http://')

    def test_import_councils(self):
        assert Council.objects.count() == 0
        cmd = MockCouncilsImporter()

        # supress output
        out = StringIO()
        cmd.stdout = out
        cmd.handle(**{'teardown': False})

        assert Council.objects.count() == 6
