# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("councils", "0002_auto_20160121_1522"),
        ("pollingstations", "0006_residentialaddress_slug"),
    ]

    operations = [
        migrations.CreateModel(
            name="DataQualityReport",
            fields=[
                (
                    "council",
                    models.OneToOneField(
                        to="councils.Council",
                        primary_key=True,
                        serialize=False,
                        on_delete=models.CASCADE,
                    ),
                ),
                ("report", models.TextField()),
            ],
        )
    ]
