# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("addressbase", "0006_auto_20170927_1215")]

    operations = [migrations.DeleteModel(name="Onsud")]
