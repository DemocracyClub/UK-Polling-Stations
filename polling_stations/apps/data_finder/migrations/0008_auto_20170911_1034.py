# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_finder', '0007_auto_20170426_0951'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CampaignSignup',
        ),
        migrations.DeleteModel(
            name='ElectionNotificationSignup',
        ),
    ]
