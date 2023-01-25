import io
import json
import sys
from unittest import TestCase, mock

import responses

from trigger.github_helpers import raise_github_issue


class GitHubHelperTests(TestCase):
    def setUp(self):
        responses.start()
        sys.stdout = io.StringIO()

    def tearDown(self):
        responses.stop()
        responses.reset()
        sys.stdout = sys.__stdout__

    def test_raise_issue_without_key(self):
        m = mock.Mock()
        with mock.patch("trigger.github_helpers.requests.post", m):
            report = {
                "gss": "X01000000",
                "council_name": "Piddleton Parish Council",
                "election_date": "2019-12-12",
                "file_set": [
                    {
                        "key": "X01000000/0000-00-00T00:00:00.00000/filename.csv",
                        "ems": "Xpress",
                    }
                ],
            }
            self.assertEqual(
                "", raise_github_issue(None, "chris48s/does-not-exist", report)
            )
            m.assert_not_called()

    def test_raise_new_issue_with_key(self):
        repo = "chris48s/does-not-exist"
        key = "f00b42"
        responses.add(
            responses.GET,
            f"https://api.github.com/repos/{repo}/issues?state=open&labels=Data%20Import",
            json=[
                {"title": "Import X01000001-Some Other Council", "number": 1232},
                {"title": "Import X01000002-Some Other Council", "number": 1233},
            ],
            status=200,
        )
        responses.add(
            responses.POST,
            f"https://api.github.com/repos/{repo}/issues",
            json={"html_url": f"https://github.com/{repo}/issues/1"},
            status=200,
        )
        report = {
            "gss": "X01000000",
            "council_name": "Piddleton Parish Council",
            "election_date": "2019-12-12",
            "file_set": [
                {
                    "key": "X01000000/0000-00-00T00:00:00.00000/filename.csv",
                    "ems": "Xpress",
                }
            ],
        }

        issue_link = raise_github_issue(key, repo, report)
        raise_issue_call = responses.calls[1]
        self.assertEqual(f"https://github.com/{repo}/issues/1", issue_link)
        self.assertEqual(
            f"https://api.github.com/repos/{repo}/issues", raise_issue_call.request.url
        )
        self.assertEqual(
            f"token {key}", raise_issue_call.request.headers["Authorization"]
        )
        self.assertDictEqual(
            {
                "title": "Import X01000000-Piddleton Parish Council for 2019-12-12",
                "body": "EMS: Xpress\nFiles:\n- `X01000000/0000-00-00T00:00:00.00000/filename.csv`",
                "labels": ["Data Import", "ready"],
            },
            json.loads(raise_issue_call.request.body),
        )

    def test_update_existing_issue_with_key(self):
        repo = "chris48s/does-not-exist"
        key = "f00b42"
        responses.add(
            responses.GET,
            f"https://api.github.com/repos/{repo}/issues?state=open&labels=Data%20Import",
            json=[
                {"title": "Import X01000001-Some Other Council", "number": 1232},
                {"title": "Import X01000002-Some Other Council", "number": 1233},
                {
                    "title": "Import X01000000-Piddleton Parish Council for 2019-12-12",
                    "number": 1234,
                },
            ],
            status=200,
        )
        responses.add(
            responses.POST,
            f"https://api.github.com/repos/{repo}/issues/1234/comments",
            json={"html_url": f"https://github.com/{repo}/issues/1234#issuecomment-1"},
            status=200,
        )
        report = {
            "gss": "X01000000",
            "council_name": "Piddleton Parish Council",
            "election_date": "2019-12-12",
            "file_set": [
                {
                    "key": "X01000000/0000-00-00T00:00:00.00000/filename.csv",
                    "ems": "Xpress",
                }
            ],
        }

        issue_link = raise_github_issue(key, repo, report)
        update_issue_call = responses.calls[1]
        self.assertEqual(
            f"https://github.com/{repo}/issues/1234#issuecomment-1", issue_link
        )
        self.assertEqual(
            f"https://api.github.com/repos/{repo}/issues/1234/comments",
            update_issue_call.request.url,
        )
        self.assertEqual(
            f"token {key}", update_issue_call.request.headers["Authorization"]
        )
        self.assertDictEqual(
            {
                "body": "Updated\nEMS: Xpress\nFiles:\n- `X01000000/0000-00-00T00:00:00.00000/filename.csv`"
            },
            json.loads(update_issue_call.request.body),
        )
