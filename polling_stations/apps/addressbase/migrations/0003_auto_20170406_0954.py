# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("addressbase", "0002_auto_20170211_1533")]

    operations = [
        migrations.CreateModel(
            name="Blacklist",
            fields=[
                (
                    "id",
                    models.AutoField(
                        serialize=False,
                        primary_key=True,
                        verbose_name="ID",
                        auto_created=True,
                    ),
                ),
                ("postcode", models.CharField(max_length=15, db_index=True)),
                ("lad", models.CharField(max_length=9)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name="blacklist", unique_together=set([("postcode", "lad")])
        ),
    ]
