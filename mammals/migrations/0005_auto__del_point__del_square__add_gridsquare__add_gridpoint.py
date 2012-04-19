# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'Point'
        db.delete_table('mammals_point')

        # Deleting model 'Square'
        db.delete_table('mammals_square')

        # Adding model 'GridSquare'
        db.create_table('mammals_gridsquare', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('NW_corner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='square_to_my_SE', to=orm['mammals.GridPoint'])),
            ('NE_corner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='square_to_my_SW', to=orm['mammals.GridPoint'])),
            ('SW_corner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='square_to_my_NE', to=orm['mammals.GridPoint'])),
            ('SE_corner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='square_to_my_NW', to=orm['mammals.GridPoint'])),
            ('label', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('mammals', ['GridSquare'])

        # Adding model 'GridPoint'
        db.create_table('mammals_gridpoint', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('geo_point', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, blank=True)),
        ))
        db.send_create_signal('mammals', ['GridPoint'])


    def backwards(self, orm):
        
        # Adding model 'Point'
        db.create_table('mammals_point', (
            ('geo_point', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('mammals', ['Point'])

        # Adding model 'Square'
        db.create_table('mammals_square', (
            ('SW_corner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='square_to_my_NE', to=orm['mammals.Point'])),
            ('NE_corner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='square_to_my_SW', to=orm['mammals.Point'])),
            ('NW_corner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='square_to_my_SE', to=orm['mammals.Point'])),
            ('SE_corner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='square_to_my_NW', to=orm['mammals.Point'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('mammals', ['Square'])

        # Deleting model 'GridSquare'
        db.delete_table('mammals_gridsquare')

        # Deleting model 'GridPoint'
        db.delete_table('mammals_gridpoint')


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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['mammals']
