# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('councils', '0002_auto_20160121_1522'),
        ('pollingstations', '0011_auto_20160501_2017'),
    ]

    operations = [
        migrations.CreateModel(
            name='ElectoralRoll',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('address', models.TextField(null=True, blank=True)),
                ('postcode', models.CharField(null=True, max_length=100, db_index=True, blank=True)),
                ('polling_district_id', models.CharField(max_length=100, blank=True)),
                ('council', models.ForeignKey(null=True, to='councils.Council')),
            ],
        ),
        migrations.AlterField(
            model_name='customfinder',
            name='area_code',
            field=models.CharField(primary_key=True, max_length=9, serialize=False, help_text='The GSS code for this area'),
        ),
        migrations.AlterField(
            model_name='customfinder',
            name='base_url',
            field=models.CharField(max_length=255, help_text='The landing page for the polling station finder', blank=True),
        ),
        migrations.AlterField(
            model_name='customfinder',
            name='can_pass_postcode',
            field=models.BooleanField(help_text="Does the URL have '?postcode=' in it?", default=False),
        ),
        migrations.AlterField(
            model_name='customfinder',
            name='message',
            field=models.TextField(default='This council has its own polling station finder:', blank=True),
        ),
        migrations.AlterField(
            model_name='pollingstation',
            name='internal_council_id',
            field=models.CharField(max_length=100, db_index=True, blank=True),
        ),
    ]
