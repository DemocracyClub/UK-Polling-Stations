# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ("councils", "0002_auto_20160121_1522"),
        ("pollingstations", "0002_pollingdistrict_polling_station_id"),
    ]

    operations = [
        migrations.CreateModel(
            name="ResidentialAddress",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("address", models.TextField(null=True, blank=True)),
                ("postcode", models.CharField(null=True, blank=True, max_length=100)),
                ("polling_station_id", models.CharField(blank=True, max_length=100)),
                (
                    "council",
                    models.ForeignKey(
                        to="councils.Council", null=True, on_delete=models.CASCADE
                    ),
                ),
            ],
        )
    ]
