# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def create_custom_finders(apps, schema_editor):
    CustomFinder = apps.get_model("pollingstations", "CustomFinder")

    CustomFinder.objects.update_or_create(
        area_code='N07000001',
        base_url='http://www.eoni.org.uk/'
                 + 'Offices/Postcode-Search-Results?postcode=',
        can_pass_postcode=True,
        message='The Electoral Office of Northern Ireland' +
                ' has its own polling station finder:',
    )


def remove_custom_finders(apps, schema_editor):
    CustomFinder = apps.get_model("pollingstations", "CustomFinder")
    CustomFinder.objects.filter(
        area_code__in=['N07000001', ]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('pollingstations', '0012_auto_20170211_1443'),
    ]

    operations = [
        migrations.RunPython(create_custom_finders, remove_custom_finders),
    ]
