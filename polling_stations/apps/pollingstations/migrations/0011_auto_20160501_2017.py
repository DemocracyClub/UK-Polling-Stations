# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("pollingstations", "0010_auto_20160417_1416")]

    operations = [
        migrations.AlterIndexTogether(
            name="pollingstation",
            index_together=set(
                [("council", "internal_council_id"), ("council", "polling_district_id")]
            ),
        )
    ]
