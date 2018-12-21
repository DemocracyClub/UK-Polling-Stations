import json
from django.test import TestCase
from django_extensions.management.commands.show_urls import Command


class UrlTests(TestCase):
    def is_exception(self, url):
        exceptions = [".txt", ".ics"]
        for exception in exceptions:
            if exception in url:
                return True
        return False

    def test_trailing_slashes(self):
        c = Command()
        data = json.loads(
            c.handle(
                **{
                    "unsorted": False,
                    "language": None,
                    "decorator": [],
                    "format_style": "json",
                    "urlconf": "ROOT_URLCONF",
                    "no_color": True,
                }
            )
        )
        urls = [rec["url"] for rec in data]
        for url in urls:
            if self.is_exception(url):
                continue
            assert url[-1] == "/", url + " does not end with /"
