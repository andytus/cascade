# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Collection'
        db.create_table(u'collection_manager_collection', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rfid', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('pickup_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('loaded_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('latitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=10, blank=True)),
            ('longitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=10, blank=True)),
        ))
        db.send_create_signal(u'collection_manager', ['Collection'])

        # Adding model 'Vehicle'
        db.create_table(u'collection_manager_vehicle', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('make', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('model', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'collection_manager', ['Vehicle'])

        # Adding model 'VehicleCollectionHistoryFile'
        db.create_table(u'collection_manager_vehiclecollectionhistoryfile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'collection_manager', ['VehicleCollectionHistoryFile'])


    def backwards(self, orm):
        # Deleting model 'Collection'
        db.delete_table(u'collection_manager_collection')

        # Deleting model 'Vehicle'
        db.delete_table(u'collection_manager_vehicle')

        # Deleting model 'VehicleCollectionHistoryFile'
        db.delete_table(u'collection_manager_vehiclecollectionhistoryfile')


    models = {
        u'collection_manager.collection': {
            'Meta': {'object_name': 'Collection'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '10', 'blank': 'True'}),
            'loaded_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '10', 'blank': 'True'}),
            'pickup_date': ('django.db.models.fields.DateTimeField', [], {}),
            'rfid': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'collection_manager.vehicle': {
            'Meta': {'object_name': 'Vehicle'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'make': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        u'collection_manager.vehiclecollectionhistoryfile': {
            'Meta': {'object_name': 'VehicleCollectionHistoryFile'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['collection_manager']