# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pollingstations', '0004_auto_20160306_1402'),
    ]

    operations = [
        migrations.AddField(
            model_name='pollingstation',
            name='polling_district_id',
            field=models.CharField(max_length=255, blank=True),
        ),
    ]
