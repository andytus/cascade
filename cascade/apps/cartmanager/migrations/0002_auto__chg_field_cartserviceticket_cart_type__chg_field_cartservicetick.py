# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'CartServiceTicket.cart_type'
        db.alter_column('cartmanager_cartserviceticket', 'cart_type', self.gf('django.db.models.fields.CharField')(max_length=25))

        # Changing field 'CartServiceTicket.service_type'
        db.alter_column('cartmanager_cartserviceticket', 'service_type', self.gf('django.db.models.fields.CharField')(max_length=25))

    def backwards(self, orm):

        # Changing field 'CartServiceTicket.cart_type'
        db.alter_column('cartmanager_cartserviceticket', 'cart_type', self.gf('django.db.models.fields.CharField')(max_length=10))

        # Changing field 'CartServiceTicket.service_type'
        db.alter_column('cartmanager_cartserviceticket', 'service_type', self.gf('django.db.models.fields.CharField')(max_length=12))

    models = {
        'cartmanager.cart': {
            'Meta': {'object_name': 'Cart'},
            'born_date': ('django.db.models.fields.DateTimeField', [], {}),
            'cart_type': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'current_status': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '10', 'blank': 'True'}),
            'last_longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '10', 'blank': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'datetime.datetime.now', 'blank': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'location'", 'null': 'True', 'to': "orm['cartmanager.CollectionAddress']"}),
            'rfid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'serial_number': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['sites.Site']"}),
            'size': ('django.db.models.fields.IntegerField', [], {})
        },
        'cartmanager.cartserviceticket': {
            'Meta': {'ordering': "['-date_created']", 'object_name': 'CartServiceTicket'},
            'audit_status': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'broken_comments': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'broken_component': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'cart': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cartmanager.Cart']", 'null': 'True', 'blank': 'True'}),
            'cart_type': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'date_completed': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_last_accessed': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'device_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '10', 'blank': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cartmanager.CollectionAddress']"}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '10', 'blank': 'True'}),
            'service_type': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['sites.Site']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'requested'", 'max_length': '12'}),
            'success_attempts': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'swap_to_rfid': ('django.db.models.fields.CharField', [], {'max_length': '24', 'null': 'True', 'blank': 'True'})
        },
        'cartmanager.cartsuploadfile': {
            'Meta': {'object_name': 'CartsUploadFile'},
            'date_end_processing': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_start_processing': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_uploaded': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'file_kind': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'file_path': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'num_error': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'num_good': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'num_records': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['sites.Site']"}),
            'size': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'PENDING'", 'max_length': '64'}),
            'total_process_time': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        },
        'cartmanager.collectionaddress': {
            'Meta': {'object_name': 'CollectionAddress'},
            'city': ('django.db.models.fields.CharField', [], {'default': "'DEFAULT'", 'max_length': '25'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cartmanager.CollectionCustomer']", 'null': 'True', 'blank': 'True'}),
            'house_number': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '10', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '10', 'blank': 'True'}),
            'route': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cartmanager.Route']", 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['sites.Site']"}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'NA'", 'max_length': '2'}),
            'street_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'Billing'", 'max_length': '9'}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'zipcode': ('django.db.models.fields.IntegerField', [], {})
        },
        'cartmanager.collectioncustomer': {
            'Meta': {'object_name': 'CollectionCustomer'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'default': "'UNKNOWN'", 'max_length': '25'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'default': "'UNKNOWN'", 'max_length': '50'}),
            'other_system_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'phone_number': ('django.contrib.localflavor.us.models.PhoneNumberField', [], {'max_length': '20', 'null': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['sites.Site']"})
        },
        'cartmanager.customersuploadfile': {
            'Meta': {'object_name': 'CustomersUploadFile'},
            'date_end_processing': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_start_processing': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_uploaded': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'file_kind': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'file_path': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'num_error': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'num_good': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'num_records': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['sites.Site']"}),
            'size': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'PENDING'", 'max_length': '64'}),
            'total_process_time': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        },
        'cartmanager.dataerrors': {
            'Meta': {'ordering': "['-error_date']", 'object_name': 'DataErrors'},
            'error_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'error_message': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'error_type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'failed_data': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'fix_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['sites.Site']"})
        },
        'cartmanager.route': {
            'Meta': {'object_name': 'Route'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'route': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'route_day': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'route_type': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['sites.Site']"})
        },
        'cartmanager.servicecenter': {
            'Meta': {'object_name': 'ServiceCenter'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'cartmanager.servicecenteraddress': {
            'Meta': {'object_name': 'ServiceCenterAddress'},
            'city': ('django.db.models.fields.CharField', [], {'default': "'DEFAULT'", 'max_length': '25'}),
            'house_number': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '10', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '10', 'blank': 'True'}),
            'route': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cartmanager.Route']", 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['sites.Site']"}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'NA'", 'max_length': '2'}),
            'street_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'zipcode': ('django.db.models.fields.IntegerField', [], {})
        },
        'cartmanager.ticketscompleteuploadfile': {
            'Meta': {'object_name': 'TicketsCompleteUploadFile'},
            'audit_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'date_end_processing': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_start_processing': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_uploaded': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'delivery_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'file_kind': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'file_path': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'num_error': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'num_good': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'num_records': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'removal_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'repair_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['sites.Site']"}),
            'size': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'PENDING'", 'max_length': '64'}),
            'swap_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'total_process_time': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'unsucessful': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'cartmanager.users': {
            'Meta': {'object_name': 'Users'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['cartmanager']