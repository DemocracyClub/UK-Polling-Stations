from django.contrib.admin.sites import AdminSite
from django.test import TestCase
from django.test.client import RequestFactory
from bug_reports.admin import BugReportAdmin
from bug_reports.models import BugReport


class BugReportAdminTest(TestCase):
    def setUp(self):
        site = AdminSite()
        self.admin = BugReportAdmin(BugReport, site)
        rf = RequestFactory()
        self.admin.request = rf.get("/foo")

    def test_valid_preview_url(self):
        record = BugReport(
            description="foo", source="wheredoivote", source_url="/privacy"
        )
        self.assertEqual(
            '<a href="http://testserver/privacy">http://testserver/privacy</a>',
            self.admin.preview_url(record),
        )

    def test_no_malicious_preview_url(self):
        record = BugReport(
            description="foo",
            source="wheredoivote",
            source_url="https://badstuff.com/steal-all-your-data",
        )
        self.assertEqual("-", self.admin.preview_url(record))
