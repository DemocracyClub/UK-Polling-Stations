# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_finder', '0002_auto_20150301_1139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataquality',
            name='council',
            field=models.OneToOneField(to='councils.Council'),
            preserve_default=True,
        ),
    ]
