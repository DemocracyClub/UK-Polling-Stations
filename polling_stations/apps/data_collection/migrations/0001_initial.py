# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [("councils", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="DataQuality",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "url",
                    models.URLField(
                        help_text=b"(PDF, website, etc)",
                        verbose_name=b"URL to the data",
                        blank=True,
                    ),
                ),
                (
                    "data_format",
                    models.CharField(
                        help_text=b"PDF, CSV, etc", max_length=100, blank=True
                    ),
                ),
                ("has_polling_stations_online", models.BooleanField(default=False)),
                ("has_polling_discricts_online", models.BooleanField(default=False)),
                (
                    "needs_manually_importing",
                    models.BooleanField(
                        default=False, help_text=b"i.e. copying and pasting from a PDF"
                    ),
                ),
                ("public_notes", models.TextField(blank=True)),
                (
                    "in_contact_with_dc",
                    models.BooleanField(
                        default=False,
                        help_text=b"Have we heard from them directly?",
                        verbose_name=b"In contact with DC?",
                    ),
                ),
                (
                    "council",
                    models.OneToOneField(
                        to="councils.Council", on_delete=models.CASCADE
                    ),
                ),
            ],
            options={"verbose_name_plural": "Data Quality"},
            bases=(models.Model,),
        )
    ]
