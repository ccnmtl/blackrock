# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.gis.db.models.fields
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Plot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('area', models.DecimalField(max_digits=10, decimal_places=2)),
                ('width', models.DecimalField(max_digits=10, decimal_places=2)),
                ('height', models.DecimalField(max_digits=10, decimal_places=2)),
                ('density', models.DecimalField(null=True, max_digits=10, decimal_places=2)),
                ('basal', models.DecimalField(null=True, max_digits=10, decimal_places=2)),
                ('num_species', models.IntegerField(null=True)),
                ('mean_dbh', models.DecimalField(null=True, max_digits=10, decimal_places=2)),
                ('variance_dbh', models.DecimalField(null=True, max_digits=10, decimal_places=2)),
                ('NW_corner', django.contrib.gis.db.models.fields.PointField(default=django.contrib.gis.geos.point.Point(), srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='Tree',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('species', models.CharField(max_length=100)),
                ('dbh', models.DecimalField(max_digits=10, decimal_places=2)),
                ('location', django.contrib.gis.db.models.fields.PointField(default=django.contrib.gis.geos.point.Point(), srid=4326)),
                ('plot', models.ForeignKey(to='optimization.Plot', on_delete=django.db.models.deletion.CASCADE)),
            ],
        ),
    ]
