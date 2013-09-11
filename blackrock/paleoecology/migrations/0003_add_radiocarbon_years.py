# flake8: noqa
# encoding: utf-8
from django.db import models
from blackrock.paleoecology.models import CoreSample
from south.db import db
from south.v2 import DataMigration
import csv
import datetime
import os

class Migration(DataMigration):

    def forwards(self, orm):
        f = open('blackrock/paleoecology/data/radiocarbon_ages_per_level.csv', 'r')

        rows = csv.reader(f)
        for row in rows:
            depth = row[0]
            try:
                core = CoreSample.objects.get(depth=depth)
                core.radiocarbon_years = row[1]
                core.save()
            except CoreSample.DoesNotExist:
                pass
        
        f.close()
        
    def backwards(self, orm):
        "No need to rollback."

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
