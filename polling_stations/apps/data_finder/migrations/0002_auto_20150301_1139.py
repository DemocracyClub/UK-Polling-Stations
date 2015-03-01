# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('councils', '0001_initial'),
        ('data_finder', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataquality',
            name='council',
            field=models.ForeignKey(default='', to='councils.Council'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='dataquality',
            name='has_polling_discricts_online',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dataquality',
            name='has_polling_stations_online',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dataquality',
            name='in_contact_with_dc',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
