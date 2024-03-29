# Generated by Django 2.2.12 on 2020-05-18 10:33

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("councils", "0005_geom_not_geog"),
    ]

    operations = [
        migrations.RenameField(
            model_name="council",
            old_name="address",
            new_name="electoral_services_address",
        ),
        migrations.RenameField(
            model_name="council",
            old_name="email",
            new_name="electoral_services_email",
        ),
        migrations.RenameField(
            model_name="council",
            old_name="postcode",
            new_name="electoral_services_postcode",
        ),
        migrations.RenameField(
            model_name="council",
            old_name="website",
            new_name="electoral_services_website",
        ),
        migrations.RemoveField(
            model_name="council",
            name="phone",
        ),
        migrations.AddField(
            model_name="council",
            name="electoral_services_phone_numbers",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=100), default=list, size=None
            ),
        ),
        migrations.AddField(
            model_name="council",
            name="identifiers",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=100), default=list, size=None
            ),
        ),
        migrations.AddField(
            model_name="council",
            name="registration_address",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="council",
            name="registration_email",
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name="council",
            name="registration_phone_numbers",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(blank=True, max_length=100),
                default=list,
                size=None,
            ),
        ),
        migrations.AddField(
            model_name="council",
            name="registration_postcode",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="council",
            name="registration_website",
            field=models.URLField(blank=True),
        ),
    ]
