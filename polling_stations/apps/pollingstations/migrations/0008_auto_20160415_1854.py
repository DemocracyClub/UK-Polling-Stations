# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pollingstations', '0007_dataqualityreport'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dataqualityreport',
            name='council',
        ),
        migrations.DeleteModel(
            name='DataQualityReport',
        ),
    ]
