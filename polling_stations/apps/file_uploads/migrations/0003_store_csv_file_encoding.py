# Generated by Django 3.2.5 on 2021-10-20 11:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("file_uploads", "0002_auto_20200203_1040"),
    ]

    operations = [
        migrations.AddField(
            model_name="file",
            name="csv_encoding",
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
