import csv
import os
from collections import namedtuple
from django.core.management.base import BaseCommand
from councils.models import Council


class Command(BaseCommand):
    def handle(self, **options):
        filename = os.path.abspath("./polling_stations/apps/councils/data/scotland.csv")
        with open(filename) as infile:
            reader = csv.reader(infile)
            Row = namedtuple("Row", next(reader))
            for row in map(Row._make, reader):
                c = Council.objects.get(pk=row.gss)
                c.email = row.email
                c.phone = row.phone
                c.website = row.web
                c.address = ""
                c.postcode = ""
                c.save()
