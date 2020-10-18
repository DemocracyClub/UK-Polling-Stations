from io import StringIO
from django.test import TestCase, override_settings
from councils.models import Council
from councils.management.commands.import_councils import Command


class MockCouncilsImporter(Command):
    def get_ons_boundary_json(self, url):
        auths = [
            {"code": "E09000001", "name": "City of London Corporation"},
            {"code": "E09000002", "name": "London Borough of Barking and Dagenham"},
            {"code": "E09000003", "name": "London Borough of Barnet"},
            {"code": "E09000004", "name": "London Borough of Bexley"},
            {"code": "E09000005", "name": "London Borough of Brent"},
            {"code": "E09000006", "name": "London Borough of Bromley"},
        ]
        out = []
        for auth in auths:
            out.append(
                {
                    "type": "Feature",
                    "properties": {
                        "objectid": 1,
                        "lad19cd": auth["code"],
                        "lad19nm": auth["name"],
                        "lad19nmw": " ",
                        "st_areashape": 123,
                        "st_lengthshape": 4564,
                    },
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [
                            [
                                [-0.354931354522705, 51.462162607847056],
                                [-0.3518199920654297, 51.462162607847056],
                                [-0.354931354522705, 51.46355294206526],
                                [-0.354931354522705, 51.462162607847056],
                            ]
                        ],
                    },
                }
            )
        return {"features": out}

    def load_contact_details(self):
        codes = [
            "E09000001",
            "E09000002",
            "E09000003",
            "E09000004",
            "E09000005",
            "E09000006",
        ]
        councils = []
        for i, code in enumerate(codes):
            councils.append(
                {
                    "code": code,
                    "official_name": "Foo {} council".format(i),
                    "electoral_services": [
                        {
                            "address": "The Electoral Office Headquarters",
                            "postcode": "BT1 1ER",
                            "tel": ["0800 4320 712"],
                            "email": "info@foo.gov.uk",
                            "website": "http://www.example.gov.uk/",
                        }
                    ],
                    "registration": None,
                    "identifiers": [code],
                },
            )
        return councils


class TestCouncilImporter(TestCase):
    @override_settings(NEW_COUNCILS=[])
    def test_import_councils(self):
        assert Council.objects.count() == 0
        cmd = MockCouncilsImporter()

        # suppress output
        out = StringIO()
        cmd.stdout = out
        cmd.handle(
            **{
                "teardown": False,
                "alt_url": None,
                "only_contact_details": False,
            }
        )

        assert Council.objects.count() == 6
