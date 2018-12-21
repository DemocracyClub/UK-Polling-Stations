# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("pollingstations", "0011_auto_20160501_2017")]

    operations = [
        migrations.AlterField(
            model_name="customfinder",
            name="area_code",
            field=models.CharField(
                serialize=False,
                help_text="The GSS code for this area",
                primary_key=True,
                max_length=9,
            ),
        ),
        migrations.AlterField(
            model_name="customfinder",
            name="base_url",
            field=models.CharField(
                blank=True,
                help_text="The landing page for the polling station finder",
                max_length=255,
            ),
        ),
        migrations.AlterField(
            model_name="customfinder",
            name="can_pass_postcode",
            field=models.BooleanField(
                help_text="Does the URL have '?postcode=' in it?", default=False
            ),
        ),
        migrations.AlterField(
            model_name="customfinder",
            name="message",
            field=models.TextField(
                blank=True, default="This council has its own polling station finder:"
            ),
        ),
        migrations.AlterField(
            model_name="pollingstation",
            name="internal_council_id",
            field=models.CharField(blank=True, db_index=True, max_length=100),
        ),
    ]
