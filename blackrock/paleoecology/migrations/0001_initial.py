# flake8: noqa
# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'CoreSample'
        db.create_table('paleoecology_coresample', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('depth', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
        ))
        db.send_create_signal('paleoecology', ['CoreSample'])

        # Adding model 'PollenType'
        db.create_table('paleoecology_pollentype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('display_name', self.gf('django.db.models.fields.CharField')(default='', unique=True, max_length=100)),
        ))
        db.send_create_signal('paleoecology', ['PollenType'])

        # Adding model 'PollenSample'
        db.create_table('paleoecology_pollensample', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('core_sample', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['paleoecology.CoreSample'])),
            ('pollen', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['paleoecology.PollenType'])),
            ('percentage', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2)),
            ('count', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2)),
        ))
        db.send_create_signal('paleoecology', ['PollenSample'])


    def backwards(self, orm):
        
        # Deleting model 'CoreSample'
        db.delete_table('paleoecology_coresample')

        # Deleting model 'PollenType'
        db.delete_table('paleoecology_pollentype')

        # Deleting model 'PollenSample'
        db.delete_table('paleoecology_pollensample')


    models = {
        'paleoecology.coresample': {
            'Meta': {'object_name': 'CoreSample'},
            'depth': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'paleoecology.pollensample': {
            'Meta': {'object_name': 'PollenSample'},
            'core_sample': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['paleoecology.CoreSample']"}),
            'count': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'percentage': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2'}),
            'pollen': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['paleoecology.PollenType']"})
        },
        'paleoecology.pollentype': {
            'Meta': {'object_name': 'PollenType'},
            'display_name': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        }
    }

    complete_apps = ['paleoecology']
