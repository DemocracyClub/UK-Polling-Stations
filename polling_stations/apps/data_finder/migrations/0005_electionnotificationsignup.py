# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [("data_finder", "0004_loggedpostcode_view_used")]

    operations = [
        migrations.CreateModel(
            name="ElectionNotificationSignup",
            fields=[
                (
                    "id",
                    models.AutoField(
                        primary_key=True,
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                    ),
                ),
                (
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, verbose_name="modified"
                    ),
                ),
                ("postcode", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254)),
                ("join_list", models.BooleanField(default=False)),
            ],
            options={
                "abstract": False,
                "ordering": ("-modified", "-created"),
                "get_latest_by": "modified",
            },
        )
    ]
