# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    replaces = [('addressbase', '0001_initial'), ('addressbase', '0002_auto_20160611_1700'), ('addressbase', '0003_auto_20160611_2130'), ('addressbase', '0004_auto_20160611_2304'), ('addressbase', '0005_auto_20160612_0904')]

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('uprn', models.CharField(primary_key=True, max_length=100, serialize=False)),
                ('address', models.TextField(blank=True)),
                ('postcode', models.CharField(db_index=True, max_length=15, blank=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(null=True, srid=4326, blank=True)),
            ],
        ),
    ]
