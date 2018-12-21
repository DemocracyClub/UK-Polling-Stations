# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("data_collection", "0008_auto_20160613_1323")]

    operations = [
        migrations.RemoveField(
            model_name="dataquality", name="postcodes_contained_by_district"
        ),
        migrations.RemoveField(
            model_name="dataquality", name="postcodes_with_addresses_generated"
        ),
    ]
