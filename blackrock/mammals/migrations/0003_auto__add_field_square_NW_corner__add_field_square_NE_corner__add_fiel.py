# flake8: noqa
# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Square.NW_corner'
        db.add_column('mammals_square', 'NW_corner', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='square_to_my_SE', to=orm['mammals.Point']), keep_default=False)

        # Adding field 'Square.NE_corner'
        db.add_column('mammals_square', 'NE_corner', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='square_to_my_SW', to=orm['mammals.Point']), keep_default=False)

        # Adding field 'Square.SW_corner'
        db.add_column('mammals_square', 'SW_corner', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='square_to_my_NE', to=orm['mammals.Point']), keep_default=False)

        # Adding field 'Square.SE_corner'
        db.add_column('mammals_square', 'SE_corner', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='square_to_my_NW', to=orm['mammals.Point']), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Square.NW_corner'
        db.delete_column('mammals_square', 'NW_corner_id')

        # Deleting field 'Square.NE_corner'
        db.delete_column('mammals_square', 'NE_corner_id')

        # Deleting field 'Square.SW_corner'
        db.delete_column('mammals_square', 'SW_corner_id')

        # Deleting field 'Square.SE_corner'
        db.delete_column('mammals_square', 'SE_corner_id')


    models = {
        'mammals.point': {
            'Meta': {'object_name': 'Point'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latlong': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True', 'default': 0})
        },
        'mammals.square': {
            'Meta': {'object_name': 'Square'},
            'NE_corner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'square_to_my_SW'", 'to': "orm['mammals.Point']"}),
            'NW_corner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'square_to_my_SE'", 'to': "orm['mammals.Point']"}),
            'SE_corner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'square_to_my_NW'", 'to': "orm['mammals.Point']"}),
            'SW_corner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'square_to_my_NE'", 'to': "orm['mammals.Point']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['mammals']
