# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'CoreSample.radiocarbon_years'
        db.add_column('paleoecology_coresample', 'radiocarbon_years', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'CoreSample.radiocarbon_years'
        db.delete_column('paleoecology_coresample', 'radiocarbon_years')


    models = {
        'paleoecology.coresample': {
            'Meta': {'object_name': 'CoreSample'},
            'depth': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'radiocarbon_years': ('django.db.models.fields.IntegerField', [], {'default': '0'})
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
