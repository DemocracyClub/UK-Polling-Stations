# Generated by Django 3.2.13 on 2022-04-19 14:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pollingstations", "0018_advancevotingstation_council"),
        ("addressbase", "0017_uprntocouncil_advance_voting_station"),
    ]

    operations = [
        migrations.AlterField(
            model_name="uprntocouncil",
            name="advance_voting_station",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="pollingstations.advancevotingstation",
            ),
        ),
    ]
