# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_finder', '0006_loggedpostcode_api_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loggedpostcode',
            name='api_user',
            field=models.CharField(null=True, max_length=30, blank=True),
        ),
    ]
