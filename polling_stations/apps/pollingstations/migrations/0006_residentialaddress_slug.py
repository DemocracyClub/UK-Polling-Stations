# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from datetime import timezone

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("pollingstations", "0005_pollingstation_polling_district_id")]

    operations = [
        migrations.AddField(
            model_name="residentialaddress",
            name="slug",
            field=models.SlugField(
                max_length=255,
                default=datetime.datetime(
                    2016, 4, 1, 21, 41, 16, 842753, tzinfo=timezone.utc
                ),
                unique=True,
            ),
            preserve_default=False,
        )
    ]
