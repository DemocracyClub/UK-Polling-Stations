# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [("data_collection", "0007_auto_20160415_1931")]

    operations = [
        migrations.AddField(
            model_name="dataquality",
            name="postcodes_contained_by_district",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="dataquality",
            name="postcodes_with_addresses_generated",
            field=models.IntegerField(default=0),
        ),
    ]
