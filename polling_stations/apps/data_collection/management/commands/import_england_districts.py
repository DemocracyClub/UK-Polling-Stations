"""
Import English Polling Districts from
May 2016 Ordnance Survey Boundary Line
to support crowdsourcing exercise.

Whereas we usually store data in the repository
boundaries for England massively exceed GitHub's
100Mb file size limit, so we must download from
Ordnance Survey and pass in path as a
command line argument.
"""

import json
import os
import shapefile
from django.contrib.gis.geos import GEOSGeometry
from django.db.utils import IntegrityError
from data_collection.management.commands import BaseShpImporter
from pollingstations.models import PollingDistrict


"""
We don't want to overwrite data we
already hold supplied by councils
there's probably scope to take a more
sophisticated approach to this in future.
This will do for now.
"""
EXCLUSIONS = [
    'E06000037',
    'E07000012',
    'E08000033',
    'E09000001',
    'E09000007',
    'E09000009',
    'E09000014',
    'S12000036',
    'W06000002',
    'W06000003',
    'W06000004',
    'W06000008',
    'W06000009',
    'W06000012',
    'W06000014',
    'W06000015',
    'W06000016',
    'W06000024'
]

"""
There are some areas with data quality problems.

I've raised a support ticket with Ordnance Survey's
Open Data Helpdesk. For the moment, I've just taken
a sledgehammer spproach and excluded all local
authorities containing one or more problematic boundaries.
"""
BAD_DATA = [
    'E06000049',
    'E06000054',
    'E06000055',
    'E06000056',
    'E07000032',
    'E07000111',
    'E07000126',
    'E07000189',
    'E07000243',
    'E08000003',
    'E08000017',
    'E08000025',
    'E09000006',
    'E09000028'
]


class Command(BaseShpImporter):

    exclusions = []
    bad_data = []
    elections = [
        'ref.2016-06-23'
    ]
    srid = 27700
    path = None
    names_codes = {}

    def add_arguments(self, parser):
        parser.add_argument(
            'path',
            help="""Path to Polling District Shapes e.g:
            '/home/user/bdline_gb-2016-05/POLLING DISTRICTS_(ENG)/Shape'"""
        )

    def district_record_to_dict(self, record):
        return {
            'internal_council_id': record[0].strip(),
            'name': "%s - %s" % (record[3].strip(), record[0].strip()),
            'council_id': self.names_codes[record[2].strip()]
        }

    def add_polling_district(self, district_info):
        # exclude records relating to:
        # the councils we already have + want to keep
        # councils with data quality issues
        if district_info['council_id'] not in self.exclusions and\
            district_info['council_id'] not in self.bad_data:
            try:
                PollingDistrict.objects.create(
                    name=district_info['name'],
                    internal_council_id=district_info['internal_council_id'],
                    extra_id='',
                    area=district_info['area'],
                    council_id=district_info['council_id'],
                    polling_station_id=''
                )
            except IntegrityError as e:
                self.stdout.write(self.style.ERROR(str(e)))

    def import_polling_districts(self):
        sf = shapefile.Reader("{0}/{1}".format(
            self.path,
            'polling_districts_England_region'
        ))
        for district in sf.shapeRecords():
            district_info = self.district_record_to_dict(district.record)
            geojson = json.dumps(district.shape.__geo_interface__)
            poly = self.clean_poly(GEOSGeometry(geojson, srid=self.get_srid('districts')))
            district_info['area'] = poly
            self.add_polling_district(district_info)

    def handle(self, *args, **kwargs):
        self.exclusions = EXCLUSIONS
        self.bad_data = BAD_DATA
        self.path = kwargs['path']

        # delete old data, excluding the councils we already have + want to keep
        PollingDistrict.objects.exclude(council__in = self.exclusions).delete()

        # load file with name -> code mappings
        with open(os.path.abspath('data/crowdsourcing/E92000001-England/names_codes.json')) as json_data:
            self.names_codes = json.load(json_data)

        self.import_polling_districts()

        # note: data quality report will be populated if and when we import stations

    def import_data(self):
        pass
