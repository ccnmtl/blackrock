# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CoreSample',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('depth', models.DecimalField(max_digits=8, decimal_places=2)),
                ('radiocarbon_years', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='PollenSample',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('percentage', models.DecimalField(null=True, max_digits=5, decimal_places=2)),
                ('count', models.DecimalField(null=True, max_digits=5, decimal_places=2)),
                ('core_sample', models.ForeignKey(to='paleoecology.CoreSample')),
            ],
        ),
        migrations.CreateModel(
            name='PollenType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('type', models.CharField(max_length=1, choices=[(b'A', b'Tree or shrub'), (b'B', b'Herb'), (b'F', b'Fern'), (b'Q', b'Aquatic (water) plant'), (b'S', b'Spore')])),
                ('display_name', models.CharField(default=b'', unique=True, max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='pollensample',
            name='pollen',
            field=models.ForeignKey(to='paleoecology.PollenType'),
        ),
    ]
