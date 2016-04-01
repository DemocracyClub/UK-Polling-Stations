# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('pollingstations', '0005_pollingstation_polling_district_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='residentialaddress',
            name='slug',
            field=models.SlugField(max_length=255, default=datetime.datetime(2016, 4, 1, 21, 41, 16, 842753, tzinfo=utc), unique=True),
            preserve_default=False,
        ),
    ]
