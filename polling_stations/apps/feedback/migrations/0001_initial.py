# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Feedback",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        verbose_name="ID",
                        primary_key=True,
                        serialize=False,
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
                        verbose_name="modified", auto_now=True
                    ),
                ),
                (
                    "found_useful",
                    models.CharField(
                        choices=[("YES", "Yes"), ("NO", "No")],
                        max_length=100,
                        blank=True,
                    ),
                ),
                ("comments", models.TextField(blank=True)),
                ("source_url", models.CharField(max_length=800, blank=True)),
                ("token", models.CharField(max_length=100, blank=True)),
            ],
            options={
                "ordering": ("-modified", "-created"),
                "abstract": False,
                "get_latest_by": "modified",
            },
        )
    ]
