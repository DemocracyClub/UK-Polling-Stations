# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields
import django_extensions.db.fields


class Migration(migrations.Migration):

    replaces = [('data_finder', '0001_initial'), ('data_finder', '0002_auto_20160315_2020'), ('data_finder', '0003_auto_20160315_2053')]

    dependencies = [
        ('councils', '0002_auto_20160121_1522'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoggedPostcode',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(verbose_name='created', auto_now_add=True)),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('postcode', models.CharField(max_length=100)),
                ('had_data', models.BooleanField(db_index=True, default=False)),
                ('council', models.ForeignKey(null=True, to='councils.Council')),
                ('location', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('brand', models.CharField(db_index=True, blank=True, max_length=100)),
                ('utm_campaign', models.CharField(db_index=True, blank=True, max_length=100)),
                ('utm_medium', models.CharField(db_index=True, blank=True, max_length=100)),
                ('utm_source', models.CharField(db_index=True, blank=True, max_length=100)),
            ],
            options={
                'abstract': False,
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
            },
        ),
    ]
