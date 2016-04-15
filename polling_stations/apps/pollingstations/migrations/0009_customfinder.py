# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pollingstations', '0006_residentialaddress_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomFinder',
            fields=[
                ('area_code', models.CharField(serialize=False, max_length=9, primary_key=True)),
                ('base_url', models.CharField(max_length=255, blank=True)),
                ('can_pass_postcode', models.BooleanField(default=False)),
                ('message', models.TextField(blank=True)),
            ],
        ),
    ]
