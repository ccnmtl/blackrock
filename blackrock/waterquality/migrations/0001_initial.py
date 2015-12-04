# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Row',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField()),
                ('value', models.DecimalField(null=True, max_digits=19, decimal_places=10)),
            ],
            options={
                'ordering': ['series', 'timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('units', models.CharField(default='', max_length=256, blank=True)),
                ('ordinality', models.IntegerField(default=0)),
                ('location', models.ForeignKey(to='waterquality.Location')),
            ],
            options={
                'ordering': ['ordinality'],
            },
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
            ],
        ),
        migrations.AddField(
            model_name='row',
            name='series',
            field=models.ForeignKey(to='waterquality.Series'),
        ),
        migrations.AddField(
            model_name='location',
            name='site',
            field=models.ForeignKey(to='waterquality.Site'),
        ),
    ]
