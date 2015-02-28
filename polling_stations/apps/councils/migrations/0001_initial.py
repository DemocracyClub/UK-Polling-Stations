# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Council',
            fields=[
                ('council_id', models.CharField(max_length=100, serialize=False, primary_key=True)),
                ('council_type', models.CharField(max_length=10, blank=True)),
                ('mapit_id', models.CharField(max_length=100, blank=True)),
                ('name', models.CharField(max_length=255, blank=True)),
                ('email', models.EmailField(max_length=75, blank=True)),
                ('phone', models.CharField(max_length=100, blank=True)),
                ('website', models.URLField(blank=True)),
                ('postcode', models.CharField(max_length=100, null=True, blank=True)),
                ('address', models.TextField(null=True, blank=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True)),
                ('area', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True, geography=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
