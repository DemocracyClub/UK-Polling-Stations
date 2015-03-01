# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataQuality',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField(blank=True)),
                ('data_format', models.CharField(max_length=100, blank=True)),
                ('has_polling_stations_online', models.BooleanField(default=True)),
                ('has_polling_discricts_online', models.BooleanField(default=True)),
                ('public_notes', models.TextField(blank=True)),
                ('in_contact_with_dc', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
