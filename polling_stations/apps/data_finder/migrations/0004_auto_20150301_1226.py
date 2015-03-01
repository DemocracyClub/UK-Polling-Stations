# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_finder', '0003_auto_20150301_1141'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dataquality',
            options={'verbose_name_plural': 'Data Quality'},
        ),
        migrations.AddField(
            model_name='dataquality',
            name='needs_manually_importing',
            field=models.BooleanField(default=False, help_text=b'i.e. copying and pasting from a PDF'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dataquality',
            name='data_format',
            field=models.CharField(help_text=b'PDF, CSV, etc', max_length=100, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dataquality',
            name='in_contact_with_dc',
            field=models.BooleanField(default=False, help_text=b'Have we heard from them directly?', verbose_name=b'In contact with DC?'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dataquality',
            name='url',
            field=models.URLField(help_text=b'(PDF, website, etc)', verbose_name=b'URL to the data', blank=True),
            preserve_default=True,
        ),
    ]
