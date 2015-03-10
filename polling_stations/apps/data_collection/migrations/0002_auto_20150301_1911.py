# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_collection', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dataquality',
            options={'ordering': ('-rating',), 'verbose_name_plural': 'Data Quality'},
        ),
        migrations.AddField(
            model_name='dataquality',
            name='rating',
            field=models.DecimalField(help_text=b'From 0 to 9', null=True, max_digits=1, decimal_places=0, blank=True),
            preserve_default=True,
        ),
    ]
