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
                ('x', models.DecimalField(max_digits=10, decimal_places=2)),
                ('y', models.DecimalField(max_digits=10, decimal_places=2)),
            ],
        ),
        migrations.CreateModel(
            name='Tree',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('species', models.CharField(max_length=100)),
                ('dbh', models.DecimalField(max_digits=10, decimal_places=2)),
                ('location', models.ForeignKey(to='sampler.Location')),
            ],
        ),
    ]
