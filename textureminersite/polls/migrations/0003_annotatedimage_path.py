# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto_20140924_2123'),
    ]

    operations = [
        migrations.AddField(
            model_name='annotatedimage',
            name='path',
            field=models.CharField(default=b'', max_length=200),
            preserve_default=True,
        ),
    ]
