# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_collection', '0003_auto_20150427_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataquality',
            name='data_format',
            field=models.CharField(max_length=100, blank=True, help_text='PDF, CSV, etc'),
        ),
        migrations.AlterField(
            model_name='dataquality',
            name='in_contact_with_dc',
            field=models.BooleanField(verbose_name='In contact with DC?', default=False, help_text='Have we heard from them directly?'),
        ),
        migrations.AlterField(
            model_name='dataquality',
            name='needs_manually_importing',
            field=models.BooleanField(default=False, help_text='i.e. copying and pasting from a PDF'),
        ),
        migrations.AlterField(
            model_name='dataquality',
            name='rating',
            field=models.DecimalField(decimal_places=0, help_text='From 0 to 9', max_digits=1, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dataquality',
            name='url',
            field=models.URLField(verbose_name='URL to the data', blank=True, help_text='(PDF, website, etc)'),
        ),
    ]
