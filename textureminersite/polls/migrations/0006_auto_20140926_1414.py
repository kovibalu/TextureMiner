# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_annotatedimage_ratio'),
    ]

    operations = [
        migrations.AddField(
            model_name='annotatedimage',
            name='height',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='annotatedimage',
            name='width',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
