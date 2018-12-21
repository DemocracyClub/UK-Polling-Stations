# -*- coding: utf-8 -*-


from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("data_collection", "0002_auto_20150301_1911")]

    operations = [
        migrations.AlterModelOptions(
            name="dataquality",
            options={"ordering": ("rating",), "verbose_name_plural": "Data Quality"},
        )
    ]
