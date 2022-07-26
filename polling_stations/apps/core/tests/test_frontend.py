from dc_utils.tests.helpers import validate_html
from django.test import TestCase
from django.urls import reverse
from addressbase.tests.factories import AddressFactory, UprnToCouncilFactory
from councils.tests.factories import CouncilFactory
from django.contrib.gis.geos import Point

import pytest

import mock


class TestHtml:
    @pytest.fixture
    def urls(self):
        CouncilFactory(
            **{
                "council_id": "BST",
                "name": "Bristol City Council",
                "electoral_services_email": "",
                "electoral_services_phone_numbers": [""],
                "electoral_services_website": "",
                "electoral_services_postcode": "",
                "electoral_services_address": "",
                "identifiers": ["E06000023"],
            }
        )
        CouncilFactory(pk="DEF", identifiers=["X01000000"])
        CouncilFactory(pk="GHI", identifiers=["X02000000"])
        # AA1 1ZZ
        UprnToCouncilFactory.create(
            lad="X01000000",
            uprn__address="1 Foo St",
            uprn__postcode="AA1 1ZZ",
            uprn__location=Point(-2.5, 50, srid=4326),
        )
        UprnToCouncilFactory.create(
            lad="X01000000",
            uprn__address="2 Foo St",
            uprn__postcode="AA1 1ZZ",
            uprn__location=Point(-2.6, 50, srid=4326),
        )
        # AA2 1ZZ
        UprnToCouncilFactory.create(
            lad="X02000000",
            uprn__address="1 Bar St",
            uprn__postcode="AA2 1ZZ",
            uprn__location=Point(-2.7, 50, srid=4326),
        )
        UprnToCouncilFactory.create(
            lad="X01000000",
            uprn__address="2 Bar St",
            uprn__postcode="AA2 1ZZ",
            uprn__location=Point(-2.8, 50, srid=4326),
        )

        return [
            reverse("home"),
            reverse("address_view", kwargs={"uprn": AddressFactory().uprn}),
            reverse("address_select_view", kwargs={"postcode": "AA1 1ZZ"}),
            reverse("dashboard:index"),
            reverse("dc_signup_form:election_reminders_signup_view"),
            reverse("example"),
            reverse("postcode_view", kwargs={"postcode": "AA1 1ZZ"}),
            reverse("we_dont_know", kwargs={"postcode": "AA1 1ZZ"}),
            reverse("multiple_councils_view", kwargs={"postcode": "AA2 1ZZ"}),
            reverse("file_uploads:councils_detail", kwargs={"pk": "GHI"}),
            reverse("feedback_form_view"),
        ]

    @pytest.mark.django_db
    @mock.patch("file_uploads.views.CouncilFileUploadAllowedMixin.test_func")
    def test_html_valid(self, test_func, admin_client, subtests, urls):
        test_func.return_value = True
        for url in urls:
            with subtests.test(msg=url):
                assert admin_client.get(url).status_code == 200
                _, errors = validate_html(admin_client, url)
                if errors:
                    print(url, errors)
                assert errors == ""


class TestBaseTemplate(TestCase):
    def test_base_template(self):
        with self.assertTemplateUsed("dc_base.html"):
            req = self.client.get("/")
            assert req.status_code == 200
            assert "dc_base_naked.html" in (t.name for t in req.templates)
