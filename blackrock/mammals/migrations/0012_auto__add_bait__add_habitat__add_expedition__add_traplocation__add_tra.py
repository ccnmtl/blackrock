# flake8: noqa
# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Bait'
        db.create_table('mammals_bait', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bait_name', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('mammals', ['Bait'])

        # Adding model 'Habitat'
        db.create_table('mammals_habitat', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('blurb', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('mammals', ['Habitat'])

        # Adding model 'Expedition'
        db.create_table('mammals_expedition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start_date_of_expedition', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('end_date_of_expedition', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='expeditions_created', null=True, to=orm['auth.User'])),
            ('notes_about_this_expedition', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('school_contact_1_phone', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('school_contact_1_email', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('school_contact_2_phone', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('school_contact_2_email', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('number_of_students', self.gf('django.db.models.fields.IntegerField')()),
            ('grade_level', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mammals.GradeLevel'], null=True, blank=True)),
            ('grid_square', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='square_to_my_SE', null=True, to=orm['mammals.GridSquare'])),
        ))
        db.send_create_signal('mammals', ['Expedition'])

        # Adding model 'TrapLocation'
        db.create_table('mammals_traplocation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('expedition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mammals.Expedition'], null=True, blank=True)),
            ('geo_point', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, blank=True)),
            ('trap_used', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mammals.Trap'], null=True, blank=True)),
            ('notes_about_location', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('habitat', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mammals.Habitat'], null=True, blank=True)),
            ('bait', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mammals.Bait'], null=True, blank=True)),
            ('animal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mammals.Animal'], null=True, blank=True)),
            ('notes_about_outcome', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('mammals', ['TrapLocation'])

        # Adding model 'Trap'
        db.create_table('mammals_trap', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('trap_string', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('mammals', ['Trap'])

        # Adding model 'Animal'
        db.create_table('mammals_animal', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('species', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mammals.Species'], null=True, blank=True)),
            ('tag_info', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('mammals', ['Animal'])

        # Adding model 'GradeLevel'
        db.create_table('mammals_gradelevel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('mammals', ['GradeLevel'])

        # Adding model 'Species'
        db.create_table('mammals_species', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('latin_name', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('common_name', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('about_this_species', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('mammals', ['Species'])


    def backwards(self, orm):
        
        # Deleting model 'Bait'
        db.delete_table('mammals_bait')

        # Deleting model 'Habitat'
        db.delete_table('mammals_habitat')

        # Deleting model 'Expedition'
        db.delete_table('mammals_expedition')

        # Deleting model 'TrapLocation'
        db.delete_table('mammals_traplocation')

        # Deleting model 'Trap'
        db.delete_table('mammals_trap')

        # Deleting model 'Animal'
        db.delete_table('mammals_animal')

        # Deleting model 'GradeLevel'
        db.delete_table('mammals_gradelevel')

        # Deleting model 'Species'
        db.delete_table('mammals_species')


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
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'species': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mammals.Species']", 'null': 'True', 'blank': 'True'}),
            'tag_info': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'mammals.bait': {
            'Meta': {'object_name': 'Bait'},
            'bait_name': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'mammals.expedition': {
            'Meta': {'object_name': 'Expedition'},
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'expeditions_created'", 'null': 'True', 'to': "orm['auth.User']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'end_date_of_expedition': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'grade_level': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mammals.GradeLevel']", 'null': 'True', 'blank': 'True'}),
            'grid_square': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'square_to_my_SE'", 'null': 'True', 'to': "orm['mammals.GridSquare']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes_about_this_expedition': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'number_of_students': ('django.db.models.fields.IntegerField', [], {}),
            'school_contact_1_email': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'school_contact_1_phone': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'school_contact_2_email': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'school_contact_2_phone': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'start_date_of_expedition': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'})
        },
        'mammals.gradelevel': {
            'Meta': {'object_name': 'GradeLevel'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'mammals.gridpoint': {
            'Meta': {'object_name': 'GridPoint'},
            'geo_point': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'mammals.gridsquare': {
            'Meta': {'object_name': 'GridSquare'},
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
            'label': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'mammals.species': {
            'Meta': {'object_name': 'Species'},
            'about_this_species': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'common_name': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latin_name': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'mammals.trap': {
            'Meta': {'object_name': 'Trap'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'trap_string': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'mammals.traplocation': {
            'Meta': {'object_name': 'TrapLocation'},
            'animal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mammals.Animal']", 'null': 'True', 'blank': 'True'}),
            'bait': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mammals.Bait']", 'null': 'True', 'blank': 'True'}),
            'expedition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mammals.Expedition']", 'null': 'True', 'blank': 'True'}),
            'geo_point': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'habitat': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mammals.Habitat']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes_about_location': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'notes_about_outcome': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'trap_used': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mammals.Trap']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['mammals']
