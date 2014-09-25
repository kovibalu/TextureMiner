# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AnnotatedImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('comp_date', models.DateTimeField(verbose_name=b'date computed')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SubImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('col', models.IntegerField(default=0)),
                ('row', models.IntegerField(default=0)),
                ('width', models.IntegerField(default=0)),
                ('height', models.IntegerField(default=0)),
                ('synth_score', models.FloatField(default=0)),
                ('imageid', models.ForeignKey(to='polls.AnnotatedImage')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
