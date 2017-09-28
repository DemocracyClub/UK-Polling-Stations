# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('uprn', models.CharField(max_length=100, serialize=False, primary_key=True)),
                ('address', models.TextField(blank=True)),
                ('postcode', models.CharField(max_length=15, db_index=True, blank=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(null=True, srid=4326, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Onsud',
            fields=[
                ('uprn', models.CharField(max_length=12, serialize=False, primary_key=True)),
                ('ctry_flag', models.CharField(max_length=1, blank=True)),
                ('cty', models.CharField(max_length=9, blank=True)),
                ('lad', models.CharField(max_length=9, blank=True)),
                ('ward', models.CharField(max_length=9, blank=True)),
                ('hlthau', models.CharField(max_length=9, blank=True)),
                ('ctry', models.CharField(max_length=9, blank=True)),
                ('rgn', models.CharField(max_length=9, blank=True)),
                ('pcon', models.CharField(max_length=9, blank=True)),
                ('eer', models.CharField(max_length=9, blank=True)),
                ('ttwa', models.CharField(max_length=9, blank=True)),
                ('nuts', models.CharField(max_length=9, blank=True)),
                ('park', models.CharField(max_length=9, blank=True)),
                ('oa11', models.CharField(max_length=9, blank=True)),
                ('lsoa11', models.CharField(max_length=9, blank=True)),
                ('msoa11', models.CharField(max_length=9, blank=True)),
                ('parish', models.CharField(max_length=9, blank=True)),
                ('wz11', models.CharField(max_length=9, blank=True)),
                ('ccg', models.CharField(max_length=9, blank=True)),
                ('bua11', models.CharField(max_length=9, blank=True)),
                ('buasd11', models.CharField(max_length=9, blank=True)),
                ('ruc11', models.CharField(max_length=2, blank=True)),
                ('oac11', models.CharField(max_length=3, blank=True)),
                ('lep1', models.CharField(max_length=9, blank=True)),
                ('lep2', models.CharField(max_length=9, blank=True)),
                ('pfa', models.CharField(max_length=9, blank=True)),
                ('imd', models.CharField(max_length=5, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
