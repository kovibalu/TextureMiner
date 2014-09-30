# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_auto_20140926_1414'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeatureValues',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('textureness', models.FloatField(default=0)),
                ('homogeneity', models.FloatField(default=0)),
                ('repetitiveness', models.FloatField(default=0)),
                ('irregularity', models.FloatField(default=0)),
                ('subimage', models.ForeignKey(to='polls.SubImage')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
