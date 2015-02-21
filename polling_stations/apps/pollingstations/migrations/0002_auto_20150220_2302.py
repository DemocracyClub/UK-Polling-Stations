# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pollingstations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pollingdistrict',
            name='area',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True, blank=True),
            preserve_default=True,
        ),
    ]
