# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("data_finder", "0005_electionnotificationsignup")]

    operations = [
        migrations.AddField(
            model_name="loggedpostcode",
            name="api_user",
            field=models.CharField(blank=True, max_length=30),
        )
    ]
