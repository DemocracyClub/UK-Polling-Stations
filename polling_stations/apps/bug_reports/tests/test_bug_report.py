from django.test import Client, TestCase
from bug_reports.models import BugReport


class TestBugReport(TestCase):

    def test_get_bug_report_view(self):
        c = Client()
        response = c.get('/report_problem/?source=foo&source_url=barbaz')
        self.assertEqual(200, response.status_code)
        expected_strings = [
            '<textarea name="description" required id="id_description" rows="3" cols="40" class=" form-control">\n</textarea>',
            '<input type="email" name="email" id="id_email" maxlength="100" class=" form-control" />',
            '<input type="submit" value="Send Report" class="button" />',
        ]
        for string in expected_strings:
            self.assertContains(response, string, html=True)

    def test_post_bug_report_view_valid_no_querystring(self):
        self.assertEqual(0, len(BugReport.objects.all()))
        c = Client()
        response = c.post('/report_problem/', {
            'source_url': '',
            'source': '',
            'description': 'some text in here',
            'email': '',
        })
        self.assertEqual(302, response.status_code)
        reports = BugReport.objects.all()
        self.assertEqual(1, len(reports))
        self.assertEqual('some text in here', reports[0].description)
        self.assertEqual('', reports[0].source_url)
        self.assertEqual('', reports[0].source)
        self.assertEqual('OPEN', reports[0].status)
        self.assertEqual('OTHER', reports[0].report_type)

    def test_post_bug_report_view_valid_with_querystring(self):
        self.assertEqual(0, len(BugReport.objects.all()))
        c = Client()
        response = c.post('/report_problem/?source=foo&source_url=barbaz', {
            'source_url': '',
            'source': '',
            'description': 'some text in here',
            'email': '',
        })
        self.assertEqual(302, response.status_code)
        reports = BugReport.objects.all()
        self.assertEqual(1, len(reports))
        self.assertEqual('some text in here', reports[0].description)
        self.assertEqual('barbaz', reports[0].source_url)
        self.assertEqual('foo', reports[0].source)
        self.assertEqual('OPEN', reports[0].status)
        self.assertEqual('OTHER', reports[0].report_type)

    def test_post_bug_report_view_invalid(self):
        self.assertEqual(0, len(BugReport.objects.all()))
        c = Client()
        response = c.post('/report_problem/?source=foo&source_url=barbaz', {
            'source_url': '',
            'source': '',
            'description': '',
            'email': '',
        })
        self.assertEqual(200, response.status_code)
        reports = BugReport.objects.all()
        self.assertEqual(0, len(reports))
        self.assertIn('<div class="form-group has-error">', str(response.content))
