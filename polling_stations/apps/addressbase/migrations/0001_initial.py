# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Address",
            fields=[
                (
                    "uprn",
                    models.CharField(primary_key=True, max_length=100, serialize=False),
                ),
                ("address", models.TextField(blank=True)),
                (
                    "postcode",
                    models.CharField(db_index=True, max_length=15, blank=True),
                ),
                (
                    "location",
                    django.contrib.gis.db.models.fields.PointField(
                        null=True, srid=4326, blank=True
                    ),
                ),
            ],
        )
    ]
