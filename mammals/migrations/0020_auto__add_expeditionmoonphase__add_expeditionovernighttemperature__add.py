# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ExpeditionMoonPhase'
        db.create_table('mammals_expeditionmoonphase', (
            ('labelmenu_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['mammals.LabelMenu'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('mammals', ['ExpeditionMoonPhase'])

        # Adding model 'ExpeditionOvernightTemperature'
        db.create_table('mammals_expeditionovernighttemperature', (
            ('labelmenu_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['mammals.LabelMenu'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('mammals', ['ExpeditionOvernightTemperature'])

        # Adding model 'AnimalScaleUsed'
        db.create_table('mammals_animalscaleused', (
            ('labelmenu_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['mammals.LabelMenu'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('mammals', ['AnimalScaleUsed'])

        # Adding model 'ExpeditionOvernightPrecipitationType'
        db.create_table('mammals_expeditionovernightprecipitationtype', (
            ('labelmenu_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['mammals.LabelMenu'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('mammals', ['ExpeditionOvernightPrecipitationType'])

        # Adding model 'ExpeditionCloudCover'
        db.create_table('mammals_expeditioncloudcover', (
            ('labelmenu_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['mammals.LabelMenu'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('mammals', ['ExpeditionCloudCover'])

        # Adding model 'LabelMenu'
        db.create_table('mammals_labelmenu', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
        ))
        db.send_create_signal('mammals', ['LabelMenu'])

        # Adding model 'ExpeditionOvernightPrecipitation'
        db.create_table('mammals_expeditionovernightprecipitation', (
            ('labelmenu_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['mammals.LabelMenu'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('mammals', ['ExpeditionOvernightPrecipitation'])

        # Adding model 'AnimalSex'
        db.create_table('mammals_animalsex', (
            ('labelmenu_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['mammals.LabelMenu'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('mammals', ['AnimalSex'])

        # Adding model 'AnimalAge'
        db.create_table('mammals_animalage', (
            ('labelmenu_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['mammals.LabelMenu'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('mammals', ['AnimalAge'])

        # Adding field 'Expedition.understory'
        db.add_column('mammals_expedition', 'understory', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True), keep_default=False)

        # Adding field 'Expedition.field_notes'
        db.add_column('mammals_expedition', 'field_notes', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True), keep_default=False)

        # Adding field 'Expedition.cloud_cover'
        db.add_column('mammals_expedition', 'cloud_cover', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='exp_cloudcover', null=True, to=orm['mammals.ExpeditionCloudCover']), keep_default=False)

        # Adding field 'Expedition.ovenight_temperature'
        db.add_column('mammals_expedition', 'ovenight_temperature', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='exp_temperature', null=True, to=orm['mammals.ExpeditionOvernightTemperature']), keep_default=False)

        # Adding field 'Expedition.ovenight_precipitation'
        db.add_column('mammals_expedition', 'ovenight_precipitation', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='exp_precipitation', null=True, to=orm['mammals.ExpeditionOvernightPrecipitation']), keep_default=False)

        # Adding field 'Expedition.ovenight_precipitation_type'
        db.add_column('mammals_expedition', 'ovenight_precipitation_type', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='exp_precipitation_type', null=True, to=orm['mammals.ExpeditionOvernightPrecipitationType']), keep_default=False)

        # Adding field 'Expedition.moon_phase'
        db.add_column('mammals_expedition', 'moon_phase', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='exp_moon_phase', null=True, to=orm['mammals.ExpeditionMoonPhase']), keep_default=False)

        # Adding unique constraint on 'GridSquare', fields ['column', 'row']
        db.create_unique('mammals_gridsquare', ['column', 'row'])

        # Adding field 'Animal.sex'
        db.add_column('mammals_animal', 'sex', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='animals_this_sex', null=True, to=orm['mammals.AnimalSex']), keep_default=False)

        # Adding field 'Animal.age'
        db.add_column('mammals_animal', 'age', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='animals_this_age', null=True, to=orm['mammals.AnimalSex']), keep_default=False)

        # Adding field 'Animal.scale_used'
        db.add_column('mammals_animal', 'scale_used', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='animals_this_scale_used', null=True, to=orm['mammals.AnimalSex']), keep_default=False)

        # Adding field 'Animal.tag_number'
        db.add_column('mammals_animal', 'tag_number', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True), keep_default=False)

        # Adding field 'Animal.health'
        db.add_column('mammals_animal', 'health', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True), keep_default=False)

        # Adding field 'Animal.weight_in_grams'
        db.add_column('mammals_animal', 'weight_in_grams', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True), keep_default=False)

        # Adding field 'Animal.recaptured'
        db.add_column('mammals_animal', 'recaptured', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Animal.scat_sample_collected'
        db.add_column('mammals_animal', 'scat_sample_collected', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Animal.blood_sample_collected'
        db.add_column('mammals_animal', 'blood_sample_collected', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Animal.hair_sample_collected'
        db.add_column('mammals_animal', 'hair_sample_collected', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Animal.skin_sample_collected'
        db.add_column('mammals_animal', 'skin_sample_collected', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)


    def backwards(self, orm):
        
        # Removing unique constraint on 'GridSquare', fields ['column', 'row']
        db.delete_unique('mammals_gridsquare', ['column', 'row'])

        # Deleting model 'ExpeditionMoonPhase'
        db.delete_table('mammals_expeditionmoonphase')

        # Deleting model 'ExpeditionOvernightTemperature'
        db.delete_table('mammals_expeditionovernighttemperature')

        # Deleting model 'AnimalScaleUsed'
        db.delete_table('mammals_animalscaleused')

        # Deleting model 'ExpeditionOvernightPrecipitationType'
        db.delete_table('mammals_expeditionovernightprecipitationtype')

        # Deleting model 'ExpeditionCloudCover'
        db.delete_table('mammals_expeditioncloudcover')

        # Deleting model 'LabelMenu'
        db.delete_table('mammals_labelmenu')

        # Deleting model 'ExpeditionOvernightPrecipitation'
        db.delete_table('mammals_expeditionovernightprecipitation')

        # Deleting model 'AnimalSex'
        db.delete_table('mammals_animalsex')

        # Deleting model 'AnimalAge'
        db.delete_table('mammals_animalage')

        # Deleting field 'Expedition.understory'
        db.delete_column('mammals_expedition', 'understory')

        # Deleting field 'Expedition.field_notes'
        db.delete_column('mammals_expedition', 'field_notes')

        # Deleting field 'Expedition.cloud_cover'
        db.delete_column('mammals_expedition', 'cloud_cover_id')

        # Deleting field 'Expedition.ovenight_temperature'
        db.delete_column('mammals_expedition', 'ovenight_temperature_id')

        # Deleting field 'Expedition.ovenight_precipitation'
        db.delete_column('mammals_expedition', 'ovenight_precipitation_id')

        # Deleting field 'Expedition.ovenight_precipitation_type'
        db.delete_column('mammals_expedition', 'ovenight_precipitation_type_id')

        # Deleting field 'Expedition.moon_phase'
        db.delete_column('mammals_expedition', 'moon_phase_id')

        # Deleting field 'Animal.sex'
        db.delete_column('mammals_animal', 'sex_id')

        # Deleting field 'Animal.age'
        db.delete_column('mammals_animal', 'age_id')

        # Deleting field 'Animal.scale_used'
        db.delete_column('mammals_animal', 'scale_used_id')

        # Deleting field 'Animal.tag_number'
        db.delete_column('mammals_animal', 'tag_number')

        # Deleting field 'Animal.health'
        db.delete_column('mammals_animal', 'health')

        # Deleting field 'Animal.weight_in_grams'
        db.delete_column('mammals_animal', 'weight_in_grams')

        # Deleting field 'Animal.recaptured'
        db.delete_column('mammals_animal', 'recaptured')

        # Deleting field 'Animal.scat_sample_collected'
        db.delete_column('mammals_animal', 'scat_sample_collected')

        # Deleting field 'Animal.blood_sample_collected'
        db.delete_column('mammals_animal', 'blood_sample_collected')

        # Deleting field 'Animal.hair_sample_collected'
        db.delete_column('mammals_animal', 'hair_sample_collected')

        # Deleting field 'Animal.skin_sample_collected'
        db.delete_column('mammals_animal', 'skin_sample_collected')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'mammals.animal': {
            'Meta': {'object_name': 'Animal'},
            'age': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'animals_this_age'", 'null': 'True', 'to': "orm['mammals.AnimalSex']"}),
            'blood_sample_collected': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'hair_sample_collected': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'health': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recaptured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'scale_used': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'animals_this_scale_used'", 'null': 'True', 'to': "orm['mammals.AnimalSex']"}),
            'scat_sample_collected': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sex': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'animals_this_sex'", 'null': 'True', 'to': "orm['mammals.AnimalSex']"}),
            'skin_sample_collected': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'species': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mammals.Species']", 'null': 'True', 'blank': 'True'}),
            'tag_info': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'tag_number': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'weight_in_grams': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'mammals.animalage': {
            'Meta': {'object_name': 'AnimalAge', '_ormbases': ['mammals.LabelMenu']},
            'labelmenu_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['mammals.LabelMenu']", 'unique': 'True', 'primary_key': 'True'})
        },
        'mammals.animalscaleused': {
            'Meta': {'object_name': 'AnimalScaleUsed', '_ormbases': ['mammals.LabelMenu']},
            'labelmenu_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['mammals.LabelMenu']", 'unique': 'True', 'primary_key': 'True'})
        },
        'mammals.animalsex': {
            'Meta': {'object_name': 'AnimalSex', '_ormbases': ['mammals.LabelMenu']},
            'labelmenu_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['mammals.LabelMenu']", 'unique': 'True', 'primary_key': 'True'})
        },
        'mammals.bait': {
            'Meta': {'object_name': 'Bait'},
            'bait_name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'mammals.expedition': {
            'Meta': {'object_name': 'Expedition'},
            'cloud_cover': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'exp_cloudcover'", 'null': 'True', 'to': "orm['mammals.ExpeditionCloudCover']"}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'expeditions_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'end_date_of_expedition': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'field_notes': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'grade_level': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mammals.GradeLevel']", 'null': 'True', 'blank': 'True'}),
            'grid_square': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'Grid Square'", 'null': 'True', 'to': "orm['mammals.GridSquare']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'moon_phase': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'exp_moon_phase'", 'null': 'True', 'to': "orm['mammals.ExpeditionMoonPhase']"}),
            'notes_about_this_expedition': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'number_of_students': ('django.db.models.fields.IntegerField', [], {}),
            'ovenight_precipitation': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'exp_precipitation'", 'null': 'True', 'to': "orm['mammals.ExpeditionOvernightPrecipitation']"}),
            'ovenight_precipitation_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'exp_precipitation_type'", 'null': 'True', 'to': "orm['mammals.ExpeditionOvernightPrecipitationType']"}),
            'ovenight_temperature': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'exp_temperature'", 'null': 'True', 'to': "orm['mammals.ExpeditionOvernightTemperature']"}),
            'school_contact_1_email': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'school_contact_1_name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'school_contact_1_phone': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'school_contact_2_email': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'school_contact_2_name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'school_contact_2_phone': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'start_date_of_expedition': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'understory': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'})
        },
        'mammals.expeditioncloudcover': {
            'Meta': {'object_name': 'ExpeditionCloudCover', '_ormbases': ['mammals.LabelMenu']},
            'labelmenu_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['mammals.LabelMenu']", 'unique': 'True', 'primary_key': 'True'})
        },
        'mammals.expeditionmoonphase': {
            'Meta': {'object_name': 'ExpeditionMoonPhase', '_ormbases': ['mammals.LabelMenu']},
            'labelmenu_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['mammals.LabelMenu']", 'unique': 'True', 'primary_key': 'True'})
        },
        'mammals.expeditionovernightprecipitation': {
            'Meta': {'object_name': 'ExpeditionOvernightPrecipitation', '_ormbases': ['mammals.LabelMenu']},
            'labelmenu_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['mammals.LabelMenu']", 'unique': 'True', 'primary_key': 'True'})
        },
        'mammals.expeditionovernightprecipitationtype': {
            'Meta': {'object_name': 'ExpeditionOvernightPrecipitationType', '_ormbases': ['mammals.LabelMenu']},
            'labelmenu_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['mammals.LabelMenu']", 'unique': 'True', 'primary_key': 'True'})
        },
        'mammals.expeditionovernighttemperature': {
            'Meta': {'object_name': 'ExpeditionOvernightTemperature', '_ormbases': ['mammals.LabelMenu']},
            'labelmenu_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['mammals.LabelMenu']", 'unique': 'True', 'primary_key': 'True'})
        },
        'mammals.gradelevel': {
            'Meta': {'object_name': 'GradeLevel'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'})
        },
        'mammals.gridpoint': {
            'Meta': {'object_name': 'GridPoint'},
            'geo_point': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'mammals.gridsquare': {
            'Meta': {'unique_together': "(('row', 'column'),)", 'object_name': 'GridSquare'},
            'NE_corner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'square_to_my_SW'", 'to': "orm['mammals.GridPoint']"}),
            'NW_corner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'square_to_my_SE'", 'to': "orm['mammals.GridPoint']"}),
            'SE_corner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'square_to_my_NW'", 'to': "orm['mammals.GridPoint']"}),
            'SW_corner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'square_to_my_NE'", 'to': "orm['mammals.GridPoint']"}),
            'access_difficulty': ('django.db.models.fields.IntegerField', [], {}),
            'center': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'square_i_am_in'", 'to': "orm['mammals.GridPoint']"}),
            'column': ('django.db.models.fields.IntegerField', [], {}),
            'display_this_square': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.IntegerField', [], {}),
            'label_2': ('django.db.models.fields.IntegerField', [], {}),
            'row': ('django.db.models.fields.IntegerField', [], {})
        },
        'mammals.habitat': {
            'Meta': {'object_name': 'Habitat'},
            'blurb': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'})
        },
        'mammals.labelmenu': {
            'Meta': {'object_name': 'LabelMenu'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'})
        },
        'mammals.species': {
            'Meta': {'object_name': 'Species'},
            'about_this_species': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'common_name': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latin_name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'})
        },
        'mammals.trap': {
            'Meta': {'object_name': 'Trap'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'trap_string': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'})
        },
        'mammals.traplocation': {
            'Meta': {'object_name': 'TrapLocation'},
            'animal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mammals.Animal']", 'null': 'True', 'blank': 'True'}),
            'bait': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mammals.Bait']", 'null': 'True', 'blank': 'True'}),
            'bait_still_there': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'expedition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mammals.Expedition']", 'null': 'True', 'blank': 'True'}),
            'geo_point': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'habitat': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mammals.Habitat']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes_about_location': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'notes_about_outcome': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'student_names': ('django.db.models.fields.TextField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'team_letter': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'team_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'transect_bearing': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'transect_distance': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'trap_used': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mammals.Trap']", 'null': 'True', 'blank': 'True'}),
            'whether_a_trap_was_set_here': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['mammals']
