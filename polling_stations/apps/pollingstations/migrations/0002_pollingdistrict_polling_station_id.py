# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pollingstations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pollingdistrict',
            name='polling_station_id',
            field=models.CharField(max_length=255, blank=True),
            preserve_default=True,
        ),
    ]
