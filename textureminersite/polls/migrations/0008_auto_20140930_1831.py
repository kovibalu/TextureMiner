# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0007_featurevalues'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeatureVector',
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
        migrations.RemoveField(
            model_name='featurevalues',
            name='subimage',
        ),
        migrations.DeleteModel(
            name='FeatureValues',
        ),
    ]
