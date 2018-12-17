# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("addressbase", "0007_delete_onsud")]

    operations = [
        migrations.CreateModel(
            name="Onsud",
            fields=[
                (
                    "uprn",
                    models.CharField(max_length=12, primary_key=True, serialize=False),
                ),
                ("ctry_flag", models.CharField(max_length=1, blank=True)),
                ("cty", models.CharField(max_length=9, blank=True)),
                ("lad", models.CharField(max_length=9, blank=True)),
                ("ward", models.CharField(max_length=9, blank=True)),
                ("hlthau", models.CharField(max_length=9, blank=True)),
                ("ctry", models.CharField(max_length=9, blank=True)),
                ("rgn", models.CharField(max_length=9, blank=True)),
                ("pcon", models.CharField(max_length=9, blank=True)),
                ("eer", models.CharField(max_length=9, blank=True)),
                ("ttwa", models.CharField(max_length=9, blank=True)),
                ("nuts", models.CharField(max_length=9, blank=True)),
                ("park", models.CharField(max_length=9, blank=True)),
                ("oa11", models.CharField(max_length=9, blank=True)),
                ("lsoa11", models.CharField(max_length=9, blank=True)),
                ("msoa11", models.CharField(max_length=9, blank=True)),
                ("parish", models.CharField(max_length=9, blank=True)),
                ("wz11", models.CharField(max_length=9, blank=True)),
                ("ccg", models.CharField(max_length=9, blank=True)),
                ("bua11", models.CharField(max_length=9, blank=True)),
                ("buasd11", models.CharField(max_length=9, blank=True)),
                ("ruc11", models.CharField(max_length=2, blank=True)),
                ("oac11", models.CharField(max_length=3, blank=True)),
                ("lep1", models.CharField(max_length=9, blank=True)),
                ("lep2", models.CharField(max_length=9, blank=True)),
                ("pfa", models.CharField(max_length=9, blank=True)),
                ("imd", models.CharField(max_length=5, blank=True)),
            ],
        ),
        migrations.AlterIndexTogether(name="onsud", index_together=set([("lad",)])),
    ]
