# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pollingstations', '0004_auto_20150228_1226'),
    ]

    operations = [
        migrations.AddField(
            model_name='pollingdistrict',
            name='internal_council_id',
            field=models.CharField(max_length=100, blank=True),
            preserve_default=True,
        ),
    ]
