# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pollingstations', '0002_auto_20150220_2302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pollingdistrict',
            name='area',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True, geography=True, blank=True),
            preserve_default=True,
        ),
    ]
