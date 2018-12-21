# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("pollingstations", "0009_customfinder")]

    operations = [
        migrations.AlterUniqueTogether(
            name="pollingdistrict",
            unique_together=set([("council", "internal_council_id")]),
        ),
        migrations.AlterUniqueTogether(
            name="pollingstation",
            unique_together=set([("council", "internal_council_id")]),
        ),
    ]
