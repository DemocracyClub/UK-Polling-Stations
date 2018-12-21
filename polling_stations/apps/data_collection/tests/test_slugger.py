from django.test import TestCase
from data_collection.slugger import Slugger


class SluggerTest(TestCase):
    def test_slugify(self):
        self.assertEqual(
            Slugger.slugify(
                " Jack & Jill like numbers 1,2,3 and 4 and silly characters ?%.$!/"
            ),
            "jack-jill-like-numbers-1-2-3-and-4-and-silly-characters-",
        )

    def test_slugify_addresses(self):
        slug1 = Slugger.slugify("5-6 Mickleton Dr, Southport")
        slug2 = Slugger.slugify("5/6, Mickleton Dr.  Southport")
        slug3 = Slugger.slugify("5-6 mickleton dr southport")
        slug4 = Slugger.slugify("56 Mickleton Dr, Southport")
        self.assertTrue((slug1 == slug2 == slug3) != slug4)

    def test_non_string_input(self):
        self.assertEqual(Slugger.slugify(123), "123")

    def test_unicode(self):
        self.assertEqual(
            Slugger.slugify("Un \xe9l\xe9phant \xe0 l'or\xe9e du bois"),
            "un-elephant-a-l-oree-du-bois",
        )
