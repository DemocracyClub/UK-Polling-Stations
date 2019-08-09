# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [("data_collection", "0005_dataquality_report")]

    operations = [
        migrations.RemoveField(model_name="dataquality", name="id"),
        migrations.AlterField(
            model_name="dataquality",
            name="council",
            field=models.OneToOneField(
                primary_key=True,
                to="councils.Council",
                serialize=False,
                on_delete=models.CASCADE,
            ),
        ),
    ]
