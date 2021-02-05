from django.test import TestCase
from rest_framework.test import APIRequestFactory
from api.councils import CouncilViewSet
from councils.tests.factories import CouncilFactory


class CouncilsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        CouncilFactory(
            council_id="ABC",
            name="ABC Council",
            electoral_services_email="",
            electoral_services_phone_numbers=[""],
            electoral_services_website="",
            electoral_services_postcode="",
            electoral_services_address="",
            identifiers=["X01000001", "E06000001"],
            geography__geography="MULTIPOLYGON (((-2.83447265625 53.64203274279828,1.549072265625 53.64203274279828,1.549072265625 52.52691653862567,-2.83447265625 52.52691653862567,-2.83447265625 53.64203274279828)))",
        )
        CouncilFactory(
            council_id="DEF",
            identifiers=["X01000002"],
            geography__geography=None,
        )

    def setUp(self):
        factory = APIRequestFactory()
        self.request = factory.get("/foo", format="json")

    def test_list(self):
        response = CouncilViewSet.as_view({"get": "list"})(self.request)
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response.data))

    def test_valid_council(self):
        response = CouncilViewSet.as_view({"get": "retrieve"})(self.request, pk="ABC")
        self.assertEqual(200, response.status_code)
        self.assertEqual("ABC", response.data["council_id"])
        self.assertEqual("England", response.data["nation"])

    def test_bad_council(self):
        response = CouncilViewSet.as_view({"get": "retrieve"})(self.request, pk="FOO")
        # should return 404 if council does not exist
        self.assertEqual(404, response.status_code)

    def test_geo(self):
        geo_response = CouncilViewSet.as_view({"get": "geo"})(self.request, pk="ABC")
        response = CouncilViewSet.as_view({"get": "retrieve"})(self.request, pk="ABC")
        # geo_response should contain geometry
        self.assertEqual(True, ("geometry" in geo_response.data))
        self.assertEqual("MultiPolygon", geo_response.data["geometry"]["type"])

        # (non-geo) response should not contain geometry
        self.assertEqual(True, ("geometry" not in response.data))

        self.assertEqual(response.data["name"], geo_response.data["properties"]["name"])

    def test_null_area(self):
        response = CouncilViewSet.as_view({"get": "geo"})(self.request, pk="DEF")
        self.assertEqual(None, response.data["geometry"])

    def test_redirect_from_identifier(self):
        """
        Check that a non-PK ID that is a valid identifier is redirected to
        the canonical URL for that instance.
        :return:
        """
        response = CouncilViewSet.as_view({"get": "retrieve"})(
            self.request, pk="X01000001"
        )
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response.url, "http://testserver/api/beta/councils/ABC/")

    def test_identifiers_in_api_response(self):
        response = CouncilViewSet.as_view({"get": "retrieve"})(self.request, pk="ABC")
        self.assertDictEqual(
            response.data,
            {
                "address": "",
                "council_id": "ABC",
                "email": "",
                "identifiers": ["X01000001", "E06000001"],
                "name": "ABC Council",
                "nation": "England",
                "phone": "",
                "postcode": "",
                "url": "http://testserver/api/beta/councils/ABC/",
                "website": "",
                "registration_contacts": None,
                "electoral_services_contacts": {
                    "email": "",
                    "phone_numbers": [""],
                    "address": "",
                    "postcode": "",
                    "website": "",
                },
            },
        )
