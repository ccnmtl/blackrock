# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
import django.contrib.gis.db.models.fields
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AssetList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('search_criteria', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Audience',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='DataSet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=500)),
                ('description', models.TextField(null=True, blank=True)),
                ('collection_start_date', models.DateField()),
                ('collection_end_date', models.DateField(null=True, blank=True)),
                ('rights_type', models.TextField(default=b'open')),
                ('spatial_explicit', models.BooleanField(default=False)),
                ('blackrock_id', models.CharField(max_length=50, unique=True, null=True, blank=True)),
                ('created_date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'created_date')),
                ('modified_date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'modified_date')),
                ('audience', models.ManyToManyField(to='portal.Audience', blank=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Data Set',
            },
        ),
        migrations.CreateModel(
            name='DigitalFormat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='DigitalObject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=500)),
                ('description', models.TextField(null=True, blank=True)),
                ('file', models.FileField(null=True, upload_to=b'portal/%Y/%m/%d/', blank=True)),
                ('url', models.URLField(null=True, blank=True)),
                ('source', models.CharField(max_length=500, null=True, blank=True)),
                ('created_date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'created_date')),
                ('modified_date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'modified_date')),
                ('markup', models.TextField(null=True, blank=True)),
                ('audience', models.ManyToManyField(to='portal.Audience', blank=True)),
                ('digital_format', models.ForeignKey(to='portal.DigitalFormat', on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Digital Object',
            },
        ),
        migrations.CreateModel(
            name='Facet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('display_name', models.CharField(max_length=100)),
                ('facet', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ['display_name'],
            },
        ),
        migrations.CreateModel(
            name='FeaturedAsset',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('detailed_display', models.BooleanField(default=False)),
                ('asset_dataset', models.ForeignKey(blank=True, to='portal.DataSet', null=True, on_delete=django.db.models.deletion.SET_NULL)),
                ('asset_digitalobject', models.ForeignKey(blank=True, to='portal.DigitalObject', null=True, on_delete=django.db.models.deletion.SET_NULL)),
            ],
        ),
        migrations.CreateModel(
            name='ForestStory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=500)),
                ('display_name', models.CharField(max_length=500)),
                ('description', models.TextField(null=True, blank=True)),
                ('file', models.FileField(null=True, upload_to=b'portal/%Y/%m/%d/', blank=True)),
                ('created_date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'created_date')),
                ('modified_date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'modified_date')),
                ('audience', models.ManyToManyField(to='portal.Audience', blank=True)),
                ('dataset', models.ManyToManyField(to='portal.DataSet', blank=True)),
                ('digital_object', models.ManyToManyField(to='portal.DigitalObject', blank=True)),
                ('display_image', models.ForeignKey(related_name='foreststory_display_image', blank=True, to='portal.DigitalObject', null=True, on_delete=django.db.models.deletion.SET_NULL)),
                ('facet', models.ManyToManyField(to='portal.Facet')),
            ],
            options={
                'ordering': ['display_name'],
                'verbose_name': 'Forest Story',
                'verbose_name_plural': 'Forest Stories',
            },
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='InteractiveMap',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='LearningActivity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=500)),
                ('description', models.TextField(null=True, blank=True)),
                ('created_date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'created_date')),
                ('modified_date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'modified_date')),
                ('audience', models.ManyToManyField(to='portal.Audience', blank=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Learning Activity',
                'verbose_name_plural': 'Learning Activities',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=500)),
                ('description', models.TextField(null=True, blank=True)),
                ('latitude', models.DecimalField(max_digits=18, decimal_places=10)),
                ('longitude', models.DecimalField(max_digits=18, decimal_places=10)),
                ('latlong', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True)),
                ('created_date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'created_date')),
                ('modified_date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'modified_date')),
                ('audience', models.ManyToManyField(to='portal.Audience', blank=True)),
                ('display_image', models.ForeignKey(blank=True, to='portal.DigitalObject', null=True, on_delete=django.db.models.deletion.SET_NULL)),
                ('facet', models.ManyToManyField(to='portal.Facet')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='LocationSubtype',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='LocationType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('full_name', models.CharField(max_length=500)),
                ('first_name', models.CharField(max_length=250)),
                ('last_name', models.CharField(max_length=250)),
                ('description', models.TextField(null=True, blank=True)),
                ('professional_title', models.CharField(max_length=100, null=True, blank=True)),
                ('address', models.TextField(null=True, blank=True)),
                ('phone', models.CharField(max_length=10, null=True, blank=True)),
                ('email', models.EmailField(max_length=254, null=True, blank=True)),
                ('url', models.URLField(null=True, blank=True)),
                ('created_date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'created_date')),
                ('modified_date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'modified_date')),
                ('audience', models.ManyToManyField(to='portal.Audience', blank=True)),
                ('display_image', models.ForeignKey(blank=True, to='portal.DigitalObject', null=True, on_delete=django.db.models.deletion.SET_NULL)),
                ('facet', models.ManyToManyField(to='portal.Facet')),
                ('institution', models.ManyToManyField(to='portal.Institution')),
            ],
            options={
                'ordering': ['last_name', 'first_name'],
                'verbose_name': 'Person',
                'verbose_name_plural': 'People',
            },
        ),
        migrations.CreateModel(
            name='PersonType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='PhotoGallery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='PhotoGalleryItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=500)),
                ('action', models.URLField()),
                ('position', models.IntegerField()),
                ('image', models.ForeignKey(related_name='gallery_display_image', blank=True, to='portal.DigitalObject', null=True, on_delete=django.db.models.deletion.SET_NULL)),
            ],
            options={
                'ordering': ('position',),
            },
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=500)),
                ('citation', models.CharField(max_length=500)),
                ('description', models.TextField(null=True, blank=True)),
                ('publication_date', models.DateField(null=True, blank=True)),
                ('url', models.URLField(null=True, blank=True)),
                ('doi_citation', models.TextField(null=True, blank=True)),
                ('created_date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'created_date')),
                ('modified_date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'modified_date')),
                ('audience', models.ManyToManyField(to='portal.Audience', blank=True)),
                ('display_image', models.ForeignKey(blank=True, to='portal.DigitalObject', null=True, on_delete=django.db.models.deletion.SET_NULL)),
                ('facet', models.ManyToManyField(to='portal.Facet')),
                ('person', models.ManyToManyField(to='portal.Person', blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='PublicationType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=500)),
                ('description', models.TextField(null=True, blank=True)),
                ('created_date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'created_date')),
                ('modified_date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'modified_date')),
                ('audience', models.ManyToManyField(to='portal.Audience', blank=True)),
                ('display_image', models.ForeignKey(blank=True, to='portal.DigitalObject', null=True, on_delete=django.db.models.deletion.SET_NULL)),
                ('facet', models.ManyToManyField(to='portal.Facet')),
                ('location', models.ManyToManyField(to='portal.Location', blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='RegionType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ResearchProject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=500)),
                ('description', models.TextField(null=True, blank=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(null=True, blank=True)),
                ('url', models.URLField(null=True, blank=True)),
                ('created_date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'created_date')),
                ('modified_date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'modified_date')),
                ('audience', models.ManyToManyField(to='portal.Audience', blank=True)),
                ('dataset', models.ManyToManyField(to='portal.DataSet', blank=True)),
                ('digital_object', models.ManyToManyField(to='portal.DigitalObject', blank=True)),
                ('display_image', models.ForeignKey(related_name='researchproject_display_image', blank=True, to='portal.DigitalObject', null=True, on_delete=django.db.models.deletion.SET_NULL)),
                ('facet', models.ManyToManyField(to='portal.Facet')),
                ('location', models.ForeignKey(blank=True, to='portal.Location', null=True, on_delete=django.db.models.deletion.SET_NULL)),
                ('person', models.ManyToManyField(to='portal.Person', blank=True)),
                ('publication', models.ManyToManyField(to='portal.Publication', blank=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Research Project',
            },
        ),
        migrations.CreateModel(
            name='RightsType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=500)),
                ('description', models.TextField(null=True, blank=True)),
                ('access_means', models.TextField(null=True, blank=True)),
                ('activation_date', models.DateField(verbose_name=b'activation_date')),
                ('created_date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'created_date')),
                ('modified_date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'modified_date')),
                ('audience', models.ManyToManyField(to='portal.Audience', blank=True)),
                ('digital_object', models.ManyToManyField(related_name='station_digital_object', to='portal.DigitalObject', blank=True)),
                ('display_image', models.ForeignKey(blank=True, to='portal.DigitalObject', null=True, on_delete=django.db.models.deletion.SET_NULL)),
                ('facet', models.ManyToManyField(to='portal.Facet')),
                ('location', models.ForeignKey(to='portal.Location', on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Station',
                'verbose_name_plural': 'Stations',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Url',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.URLField()),
                ('display_name', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Webcam',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.AddField(
            model_name='station',
            name='tag',
            field=models.ManyToManyField(to='portal.Tag', blank=True),
        ),
        migrations.AddField(
            model_name='researchproject',
            name='tag',
            field=models.ManyToManyField(to='portal.Tag', blank=True),
        ),
        migrations.AddField(
            model_name='region',
            name='region_type',
            field=models.ManyToManyField(to='portal.RegionType'),
        ),
        migrations.AddField(
            model_name='region',
            name='tag',
            field=models.ManyToManyField(to='portal.Tag', blank=True),
        ),
        migrations.AddField(
            model_name='publication',
            name='publication_type',
            field=models.ManyToManyField(to='portal.PublicationType', blank=True),
        ),
        migrations.AddField(
            model_name='publication',
            name='rights_type',
            field=models.ManyToManyField(to='portal.RightsType'),
        ),
        migrations.AddField(
            model_name='publication',
            name='tag',
            field=models.ManyToManyField(to='portal.Tag', blank=True),
        ),
        migrations.AddField(
            model_name='photogallery',
            name='item',
            field=models.ManyToManyField(to='portal.PhotoGalleryItem', blank=True),
        ),
        migrations.AddField(
            model_name='person',
            name='person_type',
            field=models.ManyToManyField(to='portal.PersonType'),
        ),
        migrations.AddField(
            model_name='person',
            name='tag',
            field=models.ManyToManyField(to='portal.Tag', blank=True),
        ),
        migrations.AddField(
            model_name='location',
            name='location_subtype',
            field=models.ManyToManyField(to='portal.LocationSubtype', blank=True),
        ),
        migrations.AddField(
            model_name='location',
            name='location_type',
            field=models.ManyToManyField(to='portal.LocationType', blank=True),
        ),
        migrations.AddField(
            model_name='location',
            name='tag',
            field=models.ManyToManyField(to='portal.Tag', blank=True),
        ),
        migrations.AddField(
            model_name='learningactivity',
            name='author',
            field=models.ManyToManyField(related_name='author', to='portal.Person'),
        ),
        migrations.AddField(
            model_name='learningactivity',
            name='dataset',
            field=models.ManyToManyField(to='portal.DataSet', blank=True),
        ),
        migrations.AddField(
            model_name='learningactivity',
            name='digital_format',
            field=models.ManyToManyField(to='portal.DigitalFormat'),
        ),
        migrations.AddField(
            model_name='learningactivity',
            name='digital_object',
            field=models.ManyToManyField(to='portal.DigitalObject', blank=True),
        ),
        migrations.AddField(
            model_name='learningactivity',
            name='display_image',
            field=models.ForeignKey(related_name='learningactivity_display_image', blank=True, to='portal.DigitalObject', null=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='learningactivity',
            name='facet',
            field=models.ManyToManyField(to='portal.Facet'),
        ),
        migrations.AddField(
            model_name='learningactivity',
            name='location',
            field=models.ForeignKey(blank=True, to='portal.Location', null=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='learningactivity',
            name='person',
            field=models.ManyToManyField(to='portal.Person', blank=True),
        ),
        migrations.AddField(
            model_name='learningactivity',
            name='tag',
            field=models.ManyToManyField(to='portal.Tag', blank=True),
        ),
        migrations.AddField(
            model_name='learningactivity',
            name='url',
            field=models.ManyToManyField(to='portal.Url', blank=True),
        ),
        migrations.AddField(
            model_name='foreststory',
            name='learning_activity',
            field=models.ManyToManyField(to='portal.LearningActivity', blank=True),
        ),
        migrations.AddField(
            model_name='foreststory',
            name='location',
            field=models.ForeignKey(blank=True, to='portal.Location', null=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='foreststory',
            name='person',
            field=models.ManyToManyField(to='portal.Person', blank=True),
        ),
        migrations.AddField(
            model_name='foreststory',
            name='publication',
            field=models.ManyToManyField(to='portal.Publication', blank=True),
        ),
        migrations.AddField(
            model_name='foreststory',
            name='research_project',
            field=models.ManyToManyField(to='portal.ResearchProject', blank=True),
        ),
        migrations.AddField(
            model_name='foreststory',
            name='station',
            field=models.ManyToManyField(related_name='foreststory_related_station', to='portal.Station', blank=True),
        ),
        migrations.AddField(
            model_name='foreststory',
            name='tag',
            field=models.ManyToManyField(to='portal.Tag', blank=True),
        ),
        migrations.AddField(
            model_name='foreststory',
            name='url',
            field=models.ManyToManyField(to='portal.Url', blank=True),
        ),
        migrations.AddField(
            model_name='featuredasset',
            name='asset_forest_story',
            field=models.ForeignKey(blank=True, to='portal.ForestStory', null=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='featuredasset',
            name='asset_learning_activity',
            field=models.ForeignKey(blank=True, to='portal.LearningActivity', null=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='featuredasset',
            name='asset_location',
            field=models.ForeignKey(blank=True, to='portal.Location', null=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='featuredasset',
            name='asset_person',
            field=models.ForeignKey(blank=True, to='portal.Person', null=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='featuredasset',
            name='asset_publication',
            field=models.ForeignKey(blank=True, to='portal.Publication', null=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='featuredasset',
            name='asset_region',
            field=models.ForeignKey(blank=True, to='portal.Region', null=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='featuredasset',
            name='asset_research_project',
            field=models.ForeignKey(blank=True, to='portal.ResearchProject', null=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='featuredasset',
            name='asset_station',
            field=models.ForeignKey(blank=True, to='portal.Station', null=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='featuredasset',
            name='audience',
            field=models.ForeignKey(to='portal.Audience', on_delete=django.db.models.deletion.CASCADE),
        ),
        migrations.AlterUniqueTogether(
            name='facet',
            unique_together=set([('name', 'facet')]),
        ),
        migrations.AddField(
            model_name='digitalobject',
            name='facet',
            field=models.ManyToManyField(to='portal.Facet'),
        ),
        migrations.AddField(
            model_name='digitalobject',
            name='tag',
            field=models.ManyToManyField(to='portal.Tag', blank=True),
        ),
        migrations.AddField(
            model_name='dataset',
            name='display_image',
            field=models.ForeignKey(blank=True, to='portal.DigitalObject', null=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='dataset',
            name='facet',
            field=models.ManyToManyField(to='portal.Facet'),
        ),
        migrations.AddField(
            model_name='dataset',
            name='location',
            field=models.ForeignKey(to='portal.Location', on_delete=django.db.models.deletion.CASCADE),
        ),
        migrations.AddField(
            model_name='dataset',
            name='person',
            field=models.ManyToManyField(to='portal.Person', blank=True),
        ),
        migrations.AddField(
            model_name='dataset',
            name='tag',
            field=models.ManyToManyField(to='portal.Tag', blank=True),
        ),
        migrations.AddField(
            model_name='dataset',
            name='url',
            field=models.ManyToManyField(to='portal.Url', blank=True),
        ),
    ]
