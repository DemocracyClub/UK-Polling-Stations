# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-23 11:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("bug_reports", "0002_auto_20180222_1659")]

    operations = [
        migrations.AlterField(
            model_name="bugreport",
            name="email",
            field=models.EmailField(
                blank=True, max_length=100, verbose_name="(Optional) Email address:"
            ),
        )
    ]
