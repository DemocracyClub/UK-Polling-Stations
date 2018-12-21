# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


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
                        to="councils.Council", primary_key=True, serialize=False
                    ),
                ),
                ("report", models.TextField()),
            ],
        )
    ]
