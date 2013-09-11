# flake8: noqa
# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Point'
        db.create_table('mammals_point', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('latlong', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, blank=True)),
        ))
        db.send_create_signal('mammals', ['Point'])

        # Adding model 'Square'
        db.create_table('mammals_square', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('mammals', ['Square'])


    def backwards(self, orm):
        
        # Deleting model 'Point'
        db.delete_table('mammals_point')

        # Deleting model 'Square'
        db.delete_table('mammals_square')


    models = {
        'mammals.point': {
            'Meta': {'object_name': 'Point'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latlong': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'})
        },
        'mammals.square': {
            'Meta': {'object_name': 'Square'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['mammals']
