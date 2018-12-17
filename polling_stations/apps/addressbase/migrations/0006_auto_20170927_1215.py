# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("addressbase", "0005_auto_20170927_1128")]

    operations = [
        migrations.CreateModel(
            name="Onsud",
            fields=[
                (
                    "uprn",
                    models.CharField(primary_key=True, max_length=12, serialize=False),
                ),
                ("ctry_flag", models.CharField(blank=True, max_length=1)),
                ("cty", models.CharField(blank=True, max_length=9)),
                ("lad", models.CharField(blank=True, max_length=9)),
                ("ward", models.CharField(blank=True, max_length=9)),
                ("hlthau", models.CharField(blank=True, max_length=9)),
                ("ctry", models.CharField(blank=True, max_length=9)),
                ("rgn", models.CharField(blank=True, max_length=9)),
                ("pcon", models.CharField(blank=True, max_length=9)),
                ("eer", models.CharField(blank=True, max_length=9)),
                ("ttwa", models.CharField(blank=True, max_length=9)),
                ("nuts", models.CharField(blank=True, max_length=9)),
                ("park", models.CharField(blank=True, max_length=9)),
                ("oa11", models.CharField(blank=True, max_length=9)),
                ("lsoa11", models.CharField(blank=True, max_length=9)),
                ("msoa11", models.CharField(blank=True, max_length=9)),
                ("parish", models.CharField(blank=True, max_length=9)),
                ("wz11", models.CharField(blank=True, max_length=9)),
                ("ccg", models.CharField(blank=True, max_length=9)),
                ("bua11", models.CharField(blank=True, max_length=9)),
                ("buasd11", models.CharField(blank=True, max_length=9)),
                ("ruc11", models.CharField(blank=True, max_length=2)),
                ("oac11", models.CharField(blank=True, max_length=3)),
                ("lep1", models.CharField(blank=True, max_length=9)),
                ("lep2", models.CharField(blank=True, max_length=9)),
                ("pfa", models.CharField(blank=True, max_length=9)),
                ("imd", models.CharField(blank=True, max_length=5)),
            ],
        ),
        migrations.DeleteModel(name="Onsad"),
    ]
