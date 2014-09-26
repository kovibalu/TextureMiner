# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_subimage_gmagavg'),
    ]

    operations = [
        migrations.AddField(
            model_name='annotatedimage',
            name='ratio',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
    ]
