# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [("pollingstations", "0003_residentialaddress")]

    operations = [
        migrations.AlterField(
            model_name="residentialaddress",
            name="postcode",
            field=models.CharField(
                null=True, db_index=True, blank=True, max_length=100
            ),
        )
    ]
