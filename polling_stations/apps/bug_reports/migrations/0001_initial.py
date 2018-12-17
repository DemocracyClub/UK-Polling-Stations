# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="BugReport",
            fields=[
                (
                    "id",
                    models.AutoField(
                        primary_key=True,
                        auto_created=True,
                        serialize=False,
                        verbose_name="ID",
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
                ("description", models.TextField()),
                ("source_url", models.CharField(blank=True, max_length=800)),
                (
                    "status",
                    models.CharField(
                        choices=[("OPEN", "Open"), ("RESOLVED", "Resolved")],
                        max_length=100,
                    ),
                ),
                ("user_agent", models.TextField(blank=True)),
                ("source", models.CharField(blank=True, max_length=100)),
                ("email", models.CharField(blank=True, max_length=100)),
                (
                    "report_type",
                    models.CharField(choices=[("OTHER", "Other")], max_length=100),
                ),
            ],
            options={
                "ordering": ("-modified", "-created"),
                "abstract": False,
                "get_latest_by": "modified",
            },
        )
    ]
