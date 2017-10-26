# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('uk_geo_utils', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Onspd',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('pcd', models.CharField(blank=True, max_length=7)),
                ('pcd2', models.CharField(blank=True, max_length=8)),
                ('pcds', models.CharField(blank=True, max_length=8)),
                ('dointr', models.CharField(blank=True, max_length=6)),
                ('doterm', models.CharField(blank=True, max_length=6)),
                ('oscty', models.CharField(blank=True, max_length=9)),
                ('oslaua', models.CharField(blank=True, max_length=9)),
                ('osward', models.CharField(blank=True, max_length=9)),
                ('usertype', models.CharField(blank=True, max_length=1)),
                ('oseast1m', models.CharField(blank=True, max_length=6)),
                ('osnrth1m', models.CharField(blank=True, max_length=7)),
                ('osgrdind', models.CharField(blank=True, max_length=1)),
                ('oshlthau', models.CharField(blank=True, max_length=9)),
                ('hro', models.CharField(blank=True, max_length=9)),
                ('ctry', models.CharField(blank=True, max_length=9)),
                ('gor', models.CharField(blank=True, max_length=9)),
                ('streg', models.CharField(blank=True, max_length=1)),
                ('pcon', models.CharField(blank=True, max_length=9)),
                ('eer', models.CharField(blank=True, max_length=9)),
                ('teclec', models.CharField(blank=True, max_length=9)),
                ('ttwa', models.CharField(blank=True, max_length=9)),
                ('pct', models.CharField(blank=True, max_length=9)),
                ('nuts', models.CharField(blank=True, max_length=10)),
                ('psed', models.CharField(blank=True, max_length=8)),
                ('cened', models.CharField(blank=True, max_length=6)),
                ('edind', models.CharField(blank=True, max_length=1)),
                ('oshaprev', models.CharField(blank=True, max_length=3)),
                ('lea', models.CharField(blank=True, max_length=3)),
                ('oldha', models.CharField(blank=True, max_length=3)),
                ('wardc91', models.CharField(blank=True, max_length=6)),
                ('wardo91', models.CharField(blank=True, max_length=6)),
                ('ward98', models.CharField(blank=True, max_length=6)),
                ('statsward', models.CharField(blank=True, max_length=6)),
                ('oa01', models.CharField(blank=True, max_length=10)),
                ('casward', models.CharField(blank=True, max_length=6)),
                ('park', models.CharField(blank=True, max_length=9)),
                ('lsoa01', models.CharField(blank=True, max_length=9)),
                ('msoa01', models.CharField(blank=True, max_length=9)),
                ('ur01ind', models.CharField(blank=True, max_length=1)),
                ('oac01', models.CharField(blank=True, max_length=3)),
                ('oldpct', models.CharField(blank=True, max_length=5)),
                ('oa11', models.CharField(blank=True, max_length=9)),
                ('lsoa11', models.CharField(blank=True, max_length=9)),
                ('msoa11', models.CharField(blank=True, max_length=9)),
                ('parish', models.CharField(blank=True, max_length=9)),
                ('wz11', models.CharField(blank=True, max_length=9)),
                ('ccg', models.CharField(blank=True, max_length=9)),
                ('bua11', models.CharField(blank=True, max_length=9)),
                ('buasd11', models.CharField(blank=True, max_length=9)),
                ('ru11ind', models.CharField(blank=True, max_length=2)),
                ('oac11', models.CharField(blank=True, max_length=3)),
                ('lat', models.CharField(blank=True, max_length=10)),
                ('long', models.CharField(blank=True, max_length=10)),
                ('lep1', models.CharField(blank=True, max_length=9)),
                ('lep2', models.CharField(blank=True, max_length=9)),
                ('pfa', models.CharField(blank=True, max_length=9)),
                ('imd', models.CharField(blank=True, max_length=5)),
                ('location', django.contrib.gis.db.models.fields.PointField(null=True, blank=True, srid=4326)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
