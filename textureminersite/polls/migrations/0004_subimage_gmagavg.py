# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_annotatedimage_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='subimage',
            name='gmagavg',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
    ]
