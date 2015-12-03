# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StationMapping',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('abbreviation', models.CharField(max_length=5)),
                ('station', models.CharField(unique=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Temperature',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('station', models.CharField(max_length=50, unique_for_date=b'date')),
                ('date', models.DateTimeField()),
                ('reading', models.FloatField(null=True, blank=True)),
                ('precalc', models.FloatField(null=True, blank=True)),
                ('data_source', models.CharField(max_length=10, choices=[(b'original', b'Original Blackrock Spreadsheet'), (b'mock', b'Mock data to fill in gaps')])),
            ],
        ),
    ]
