# Generated by Django 2.2.12 on 2020-05-18 21:33

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("addressbase", "0014_uprntocouncil_polling_station_id"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Blacklist",
        ),
    ]
