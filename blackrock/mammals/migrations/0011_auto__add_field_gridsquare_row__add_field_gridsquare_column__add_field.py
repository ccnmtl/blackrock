# flake8: noqa
# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'GridSquare.row'
        db.add_column('mammals_gridsquare', 'row', self.gf('django.db.models.fields.IntegerField')(default=1), keep_default=False)

        # Adding field 'GridSquare.column'
        db.add_column('mammals_gridsquare', 'column', self.gf('django.db.models.fields.IntegerField')(default=1), keep_default=False)

        # Adding field 'GridSquare.access_difficulty'
        db.add_column('mammals_gridsquare', 'access_difficulty', self.gf('django.db.models.fields.IntegerField')(default=1), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'GridSquare.row'
        db.delete_column('mammals_gridsquare', 'row')

        # Deleting field 'GridSquare.column'
        db.delete_column('mammals_gridsquare', 'column')

        # Deleting field 'GridSquare.access_difficulty'
        db.delete_column('mammals_gridsquare', 'access_difficulty')


    models = {
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
        }
    }

    complete_apps = ['mammals']
