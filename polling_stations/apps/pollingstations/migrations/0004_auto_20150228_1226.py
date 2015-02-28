# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('councils', '0001_initial'),
        ('pollingstations', '0003_auto_20150221_0003'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pollingdistrict',
            name='council_id',
        ),
        migrations.AddField(
            model_name='pollingdistrict',
            name='council',
            field=models.ForeignKey(default='', to='councils.Council'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pollingstation',
            name='council',
            field=models.ForeignKey(default='', to='councils.Council'),
            preserve_default=False,
        ),
    ]
