# Generated by Django 2.2.16 on 2020-12-08 21:17

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("bug_reports", "0003_auto_20180223_1148"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="bugreport",
            options={"get_latest_by": "modified"},
        ),
    ]
