from unittest import TestCase

from core.cache import key_function


class CacheTest(TestCase):
    def test_key_function(self):
        self.assertEqual(
            key_function(
                "django_cache",
                "http://localhost:8001/api/elections.json?postcode=B12 8UD&future=1&current=1",
                "1",
            ),
            "django_cache:http://localhost:8001/api/elections.json?postcode=B128UD&future=1&current=1:1",
        )
