# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Point.latlong'
        db.delete_column('mammals_point', 'latlong')

        # Adding field 'Point.geo_point'
        db.add_column('mammals_point', 'geo_point', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Adding field 'Point.latlong'
        db.add_column('mammals_point', 'latlong', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, blank=True), keep_default=False)

        # Deleting field 'Point.geo_point'
        db.delete_column('mammals_point', 'geo_point')


    models = {
        'mammals.point': {
            'Meta': {'object_name': 'Point'},
            'geo_point': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
