# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.gis.db.models.fields
import django.db.models.deletion
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Animal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField(help_text=b'age / sex / other notes', blank=True)),
                ('tag_number', models.CharField(default=b'', max_length=256, null=True, blank=True)),
                ('health', models.CharField(default=b'', max_length=256, null=True, blank=True)),
                ('weight_in_grams', models.IntegerField(default=None, null=True, blank=True)),
                ('recaptured', models.BooleanField(default=False)),
                ('scat_sample_collected', models.BooleanField(default=False)),
                ('blood_sample_collected', models.BooleanField(default=False)),
                ('hair_sample_collected', models.BooleanField(default=False)),
                ('skin_sample_collected', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Bait',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bait_name', models.CharField(help_text=b'Label for the type of bait', max_length=256, blank=True)),
            ],
            options={
                'ordering': ['bait_name'],
                'verbose_name': 'Bait type used',
                'verbose_name_plural': 'Types of bait used',
            },
        ),
        migrations.CreateModel(
            name='Expedition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date_of_expedition', models.DateTimeField(auto_now_add=True, null=True)),
                ('end_date_of_expedition', models.DateTimeField(auto_now_add=True, null=True)),
                ('real', models.BooleanField(default=True, help_text=b'Is this expedition real or just a test?')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('notes_about_this_expedition', models.TextField(help_text=b'Notes about this expedition', blank=True)),
                ('school_contact_1_name', models.CharField(help_text=b'First contact @ the school -- name', max_length=256, blank=True)),
                ('school_contact_1_phone', models.CharField(help_text=b'First contact @ the school -- e-mail', max_length=256, blank=True)),
                ('school_contact_1_email', models.CharField(help_text=b'First contact @ the school -- phone', max_length=256, blank=True)),
                ('number_of_students', models.IntegerField(default=0, help_text=b'How many students participated')),
                ('field_notes', models.CharField(max_length=1024, null=True, blank=True)),
                ('overnight_temperature_int', models.IntegerField(default=0, help_text=b'Overnight Temperature')),
                ('created_by', models.ForeignKey(related_name='expeditions_created', blank=True, to=settings.AUTH_USER_MODEL, null=True, on_delete=django.db.models.deletion.SET_NULL)),
            ],
            options={
                'ordering': ['-end_date_of_expedition'],
            },
        ),
        migrations.CreateModel(
            name='GradeLevel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(help_text=b'The name of the grade level', max_length=256, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='GridPoint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('geo_point', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='GridSquare',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('display_this_square', models.BooleanField(default=False)),
                ('row', models.IntegerField()),
                ('column', models.IntegerField()),
                ('access_difficulty', models.IntegerField(default=0, help_text=b'is the overall difficulty and length of time for a group\n        of students to get to the square from the Science Center.', verbose_name=b'Access Difficulty')),
                ('terrain_difficulty', models.IntegerField(default=0, help_text=b'How rough the terrain is on this square.', verbose_name=b'Terrain Difficulty')),
                ('NE_corner', models.ForeignKey(related_name='square_to_my_SW', verbose_name=b'Northeast corner', to='mammals.GridPoint', on_delete=django.db.models.deletion.CASCADE)),
                ('NW_corner', models.ForeignKey(related_name='square_to_my_SE', verbose_name=b'Northwest corner', to='mammals.GridPoint', on_delete=django.db.models.deletion.CASCADE)),
                ('SE_corner', models.ForeignKey(related_name='square_to_my_NW', verbose_name=b'Southeast corner', to='mammals.GridPoint', on_delete=django.db.models.deletion.CASCADE)),
                ('SW_corner', models.ForeignKey(related_name='square_to_my_NE', verbose_name=b'Southwest corner', to='mammals.GridPoint', on_delete=django.db.models.deletion.CASCADE)),
                ('center', models.ForeignKey(related_name='square_i_am_in', verbose_name=b'Center point', to='mammals.GridPoint', on_delete=django.db.models.deletion.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='Habitat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(help_text=b'Short label for this habitat.', max_length=256, blank=True)),
                ('blurb', models.TextField(help_text=b'Notes about this habitat (for a habitat page).', blank=True)),
                ('image_path_for_legend', models.CharField(help_text=b'Path to the round colored circle for this habitat', max_length=256, blank=True)),
                ('color_for_map', models.CharField(help_text=b'RGB color to use on the map', max_length=3, blank=True)),
            ],
            options={
                'ordering': ['label'],
            },
        ),
        migrations.CreateModel(
            name='LabelMenu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=256, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', help_text=b'Name of school', max_length=256, blank=True)),
                ('address', models.CharField(default=b'', help_text=b'Name of school', max_length=256, blank=True)),
                ('contact_1_name', models.CharField(help_text=b'First contact @ the school -- name', max_length=256, blank=True)),
                ('contact_1_phone', models.CharField(help_text=b'First contact @ the school -- e-mail', max_length=256, blank=True)),
                ('contact_1_email', models.CharField(help_text=b'First contact @ the school   -- phone', max_length=256, blank=True)),
                ('contact_2_name', models.CharField(help_text=b'First contact @ the school -- name', max_length=256, blank=True)),
                ('contact_2_phone', models.CharField(help_text=b'Second contact @ the school  -- e-mail', max_length=256, blank=True)),
                ('contact_2_email', models.CharField(help_text=b'Second contact @ the school  -- phone', max_length=256, blank=True)),
                ('notes', models.CharField(help_text=b'Any other notes about this school.', max_length=256, blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Sighting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(help_text=b'Where the animal was seen', srid=4326, null=True, blank=True)),
                ('date', models.DateTimeField(help_text=b'Where the animal was seen', auto_now_add=True, null=True)),
                ('observers', models.TextField(default=None, help_text=b'Initials of the people who made the observation.', null=True, blank=True)),
                ('how_many_observed', models.IntegerField(default=None, help_text=b'How many animals were observed, if applicable.', null=True, blank=True)),
                ('notes', models.TextField(default=None, help_text=b'Notes about the location', null=True, blank=True)),
                ('habitat', models.ForeignKey(blank=True, to='mammals.Habitat', help_text=b'What habitat best describes this location?', null=True, on_delete=django.db.models.deletion.SET_NULL)),
            ],
        ),
        migrations.CreateModel(
            name='Species',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('latin_name', models.CharField(help_text=b'Binomial species name', max_length=256, blank=True)),
                ('common_name', models.CharField(help_text=b'Common name', max_length=512, blank=True)),
                ('about_this_species', models.TextField(help_text=b'A blurb with info about this species at Blackrock', blank=True)),
            ],
            options={
                'ordering': ['common_name'],
                'verbose_name': 'Species',
                'verbose_name_plural': 'Species',
            },
        ),
        migrations.CreateModel(
            name='Trap',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('trap_string', models.CharField(help_text=b'This should be a unique string to identify each trap.', max_length=256, blank=True)),
                ('notes', models.CharField(help_text=b'Notes about this trap.', max_length=256, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='TrapLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('suggested_point', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True)),
                ('actual_point', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True)),
                ('understory', models.TextField(default=b'', help_text=b'Understory', null=True, blank=True)),
                ('notes_about_location', models.TextField(help_text=b'Notes about the location', blank=True)),
                ('transect_bearing', models.FloatField(help_text=b'Heading of this bearing', null=True, blank=True)),
                ('transect_distance', models.FloatField(help_text=b'Distance along this bearing', null=True, blank=True)),
                ('team_letter', models.CharField(help_text=b'Name of team responsible for this location.', max_length=256, null=True, blank=True)),
                ('team_number', models.IntegerField(help_text=b'Differentiates the traps each team is in charge of.', null=True, blank=True)),
                ('order', models.IntegerField(help_text=b'Order in which to show this trap.', null=True, blank=True)),
                ('whether_a_trap_was_set_here', models.BooleanField(default=False, help_text=b"We typically won't use all the locations suggested by the\n        randomization recipe; this denotes that a trap was actually placed at\n        or near this point.")),
                ('bait_still_there', models.BooleanField(default=False, help_text=b'Was the bait you left in the trap still there\n        when you came back?')),
                ('notes_about_outcome', models.TextField(help_text=b'Any miscellaneous notes about the outcome', blank=True)),
                ('student_names', models.TextField(help_text=b'Names of the students responsible for this location\n        (this would be filled in, if at all, by the instructor after the\n        students have left the forest.', max_length=256, null=True, blank=True)),
                ('animal', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='mammals.Animal', help_text=b'Any animals caught', null=True)),
                ('bait', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='mammals.Bait', help_text=b'Any bait used', null=True)),
                ('expedition', models.ForeignKey(blank=True, to='mammals.Expedition', null=True, on_delete=django.db.models.deletion.SET_NULL)),
                ('habitat', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='mammals.Habitat', help_text=b'What habitat best describes this location?', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AnimalAge',
            fields=[
                ('labelmenu_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='mammals.LabelMenu', on_delete=django.db.models.deletion.CASCADE)),
            ],
            bases=('mammals.labelmenu',),
        ),
        migrations.CreateModel(
            name='AnimalScaleUsed',
            fields=[
                ('labelmenu_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='mammals.LabelMenu', on_delete=django.db.models.deletion.CASCADE)),
            ],
            bases=('mammals.labelmenu',),
        ),
        migrations.CreateModel(
            name='AnimalSex',
            fields=[
                ('labelmenu_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='mammals.LabelMenu', on_delete=django.db.models.deletion.CASCADE)),
            ],
            bases=('mammals.labelmenu',),
        ),
        migrations.CreateModel(
            name='ExpeditionCloudCover',
            fields=[
                ('labelmenu_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='mammals.LabelMenu', on_delete=django.db.models.deletion.CASCADE)),
            ],
            bases=('mammals.labelmenu',),
        ),
        migrations.CreateModel(
            name='ExpeditionMoonPhase',
            fields=[
                ('labelmenu_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='mammals.LabelMenu', on_delete=django.db.models.deletion.CASCADE)),
            ],
            bases=('mammals.labelmenu',),
        ),
        migrations.CreateModel(
            name='ExpeditionOvernightPrecipitation',
            fields=[
                ('labelmenu_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='mammals.LabelMenu', on_delete=django.db.models.deletion.CASCADE)),
            ],
            bases=('mammals.labelmenu',),
        ),
        migrations.CreateModel(
            name='ExpeditionOvernightPrecipitationType',
            fields=[
                ('labelmenu_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='mammals.LabelMenu', on_delete=django.db.models.deletion.CASCADE)),
            ],
            bases=('mammals.labelmenu',),
        ),
        migrations.CreateModel(
            name='ExpeditionOvernightTemperature',
            fields=[
                ('labelmenu_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='mammals.LabelMenu', on_delete=django.db.models.deletion.CASCADE)),
            ],
            bases=('mammals.labelmenu',),
        ),
        migrations.CreateModel(
            name='Illumination',
            fields=[
                ('labelmenu_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='mammals.LabelMenu', on_delete=django.db.models.deletion.CASCADE)),
            ],
            bases=('mammals.labelmenu',),
        ),
        migrations.CreateModel(
            name='ObservationType',
            fields=[
                ('labelmenu_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='mammals.LabelMenu', on_delete=django.db.models.deletion.CASCADE)),
            ],
            bases=('mammals.labelmenu',),
        ),
        migrations.CreateModel(
            name='TrapType',
            fields=[
                ('labelmenu_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='mammals.LabelMenu', on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'ordering': ['label'],
            },
            bases=('mammals.labelmenu',),
        ),
        migrations.AddField(
            model_name='sighting',
            name='species',
            field=models.ForeignKey(blank=True, to='mammals.Species', help_text=b'Best guess at species.', null=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='expedition',
            name='grade_level',
            field=models.ForeignKey(blank=True, to='mammals.GradeLevel', null=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='expedition',
            name='grid_square',
            field=models.ForeignKey(related_name='Grid Square+', verbose_name=b'Grid Square used for this expedition', blank=True, to='mammals.GridSquare', null=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='expedition',
            name='school',
            field=models.ForeignKey(blank=True, to='mammals.School', null=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='animal',
            name='species',
            field=models.ForeignKey(blank=True, to='mammals.Species', null=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='traplocation',
            name='trap_type',
            field=models.ForeignKey(blank=True, to='mammals.TrapType', help_text=b'Which type of trap, if any, was left at this location.', null=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='sighting',
            name='observation_type',
            field=models.ForeignKey(blank=True, to='mammals.ObservationType', help_text=b'e.g. sighting, camera-trapped, etc.', null=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AlterUniqueTogether(
            name='gridsquare',
            unique_together=set([('row', 'column')]),
        ),
        migrations.AddField(
            model_name='expedition',
            name='cloud_cover',
            field=models.ForeignKey(related_name='exp_cloudcover', blank=True, to='mammals.ExpeditionCloudCover', null=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='expedition',
            name='illumination',
            field=models.ForeignKey(related_name='exp_illumination', blank=True, to='mammals.Illumination', null=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='expedition',
            name='moon_phase',
            field=models.ForeignKey(related_name='exp_moon_phase', blank=True, to='mammals.ExpeditionMoonPhase', null=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='expedition',
            name='overnight_precipitation',
            field=models.ForeignKey(related_name='exp_precipitation', blank=True, to='mammals.ExpeditionOvernightPrecipitation', null=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='expedition',
            name='overnight_precipitation_type',
            field=models.ForeignKey(related_name='exp_precipitation_type', blank=True, to='mammals.ExpeditionOvernightPrecipitationType', null=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='expedition',
            name='overnight_temperature',
            field=models.ForeignKey(related_name='exp_temperature', blank=True, to='mammals.ExpeditionOvernightTemperature', null=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='animal',
            name='age',
            field=models.ForeignKey(related_name='animals_this_age', verbose_name=b'Age of this animal', blank=True, to='mammals.AnimalAge', null=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='animal',
            name='scale_used',
            field=models.ForeignKey(related_name='animals_this_scale_used', verbose_name=b'Scale used to weigh this animal', blank=True, to='mammals.AnimalScaleUsed', null=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='animal',
            name='sex',
            field=models.ForeignKey(related_name='animals_this_sex', verbose_name=b'Sex of this animal', blank=True, to='mammals.AnimalSex', null=True, on_delete=django.db.models.deletion.SET_NULL),
        ),
    ]
