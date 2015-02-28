# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pollingstations', '0005_pollingdistrict_internal_council_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pollingdistrict',
            name='council',
            field=models.ForeignKey(to='councils.Council', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pollingstation',
            name='council',
            field=models.ForeignKey(to='councils.Council', null=True),
            preserve_default=True,
        ),
    ]
