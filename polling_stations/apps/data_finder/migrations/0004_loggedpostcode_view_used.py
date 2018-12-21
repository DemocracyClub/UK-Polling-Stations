# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [("data_finder", "0003_loggedpostcode_language")]

    operations = [
        migrations.AddField(
            model_name="loggedpostcode",
            name="view_used",
            field=models.CharField(max_length=100, blank=True),
        )
    ]
