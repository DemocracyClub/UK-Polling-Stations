# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_finder', '0002_campaignsignup'),
    ]

    operations = [
        migrations.AddField(
            model_name='loggedpostcode',
            name='language',
            field=models.CharField(max_length=5, blank=True),
        ),
    ]
