# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Route'
        db.create_table('cartmanager_route', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('route', self.gf('django.db.models.fields.CharField')(max_length=15, null=True)),
            ('route_day', self.gf('django.db.models.fields.CharField')(max_length=15, null=True)),
            ('route_type', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
        ))
        db.send_create_signal('cartmanager', ['Route'])

        # Adding model 'ServiceCenter'
        db.create_table('cartmanager_servicecenter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('cartmanager', ['ServiceCenter'])

        # Adding model 'ServiceCenterAddress'
        db.create_table('cartmanager_servicecenteraddress', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('house_number', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('street_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('unit', self.gf('django.db.models.fields.CharField')(max_length=6, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(default='DEFAULT', max_length=25)),
            ('state', self.gf('django.db.models.fields.CharField')(default='NA', max_length=2)),
            ('zipcode', self.gf('django.db.models.fields.IntegerField')()),
            ('latitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=10, blank=True)),
            ('longitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=10, blank=True)),
            ('route', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cartmanager.Route'], null=True, blank=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
        ))
        db.send_create_signal('cartmanager', ['ServiceCenterAddress'])

        # Adding model 'CollectionCustomer'
        db.create_table('cartmanager_collectioncustomer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('other_system_id', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('first_name', self.gf('django.db.models.fields.CharField')(default='UNKNOWN', max_length=25)),
            ('last_name', self.gf('django.db.models.fields.CharField')(default='UNKNOWN', max_length=50)),
            ('phone_number', self.gf('django.contrib.localflavor.us.models.PhoneNumberField')(max_length=20, null=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
        ))
        db.send_create_signal('cartmanager', ['CollectionCustomer'])

        # Adding model 'CollectionAddress'
        db.create_table('cartmanager_collectionaddress', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('house_number', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('street_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('unit', self.gf('django.db.models.fields.CharField')(max_length=6, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(default='DEFAULT', max_length=25)),
            ('state', self.gf('django.db.models.fields.CharField')(default='NA', max_length=2)),
            ('zipcode', self.gf('django.db.models.fields.IntegerField')()),
            ('latitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=10, blank=True)),
            ('longitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=10, blank=True)),
            ('route', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cartmanager.Route'], null=True, blank=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
            ('type', self.gf('django.db.models.fields.CharField')(default='Billing', max_length=9)),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cartmanager.CollectionCustomer'], null=True, blank=True)),
        ))
        db.send_create_signal('cartmanager', ['CollectionAddress'])

        # Adding model 'Cart'
        db.create_table('cartmanager_cart', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='location', null=True, to=orm['cartmanager.CollectionAddress'])),
            ('last_latitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=10, blank=True)),
            ('last_longitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=10, blank=True)),
            ('rfid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('serial_number', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('size', self.gf('django.db.models.fields.IntegerField')()),
            ('current_status', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('cart_type', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=datetime.datetime.now, blank=True)),
            ('born_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
        ))
        db.send_create_signal('cartmanager', ['Cart'])

        # Adding model 'CartServiceTicket'
        db.create_table('cartmanager_cartserviceticket', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cartmanager.CollectionAddress'])),
            ('cart', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cartmanager.Cart'], null=True, blank=True)),
            ('service_type', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('cart_type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('status', self.gf('django.db.models.fields.CharField')(default='requested', max_length=12)),
            ('date_completed', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_last_accessed', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('latitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=10, blank=True)),
            ('longitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=10, blank=True)),
            ('device_name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('swap_to_rfid', self.gf('django.db.models.fields.CharField')(max_length=24, null=True, blank=True)),
            ('success_attempts', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('audit_status', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('broken_component', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('broken_comments', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
        ))
        db.send_create_signal('cartmanager', ['CartServiceTicket'])

        # Adding model 'Users'
        db.create_table('cartmanager_users', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('cartmanager', ['Users'])

        # Adding model 'CartsUploadFile'
        db.create_table('cartmanager_cartsuploadfile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('size', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('date_uploaded', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='PENDING', max_length=64)),
            ('num_records', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('num_good', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('num_error', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('date_start_processing', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('date_end_processing', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('total_process_time', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('file_kind', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
            ('file_path', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal('cartmanager', ['CartsUploadFile'])

        # Adding model 'TicketsCompleteUploadFile'
        db.create_table('cartmanager_ticketscompleteuploadfile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('size', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('date_uploaded', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='PENDING', max_length=64)),
            ('num_records', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('num_good', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('num_error', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('date_start_processing', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('date_end_processing', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('total_process_time', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('file_kind', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
            ('file_path', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('swap_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('delivery_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('removal_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('audit_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('unsucessful', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('repair_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('cartmanager', ['TicketsCompleteUploadFile'])

        # Adding model 'CustomersUploadFile'
        db.create_table('cartmanager_customersuploadfile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('size', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('date_uploaded', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='PENDING', max_length=64)),
            ('num_records', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('num_good', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('num_error', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('date_start_processing', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('date_end_processing', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('total_process_time', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('file_kind', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
            ('file_path', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal('cartmanager', ['CustomersUploadFile'])

        # Adding model 'DataErrors'
        db.create_table('cartmanager_dataerrors', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('error_message', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('error_type', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('failed_data', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('error_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('fix_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
        ))
        db.send_create_signal('cartmanager', ['DataErrors'])


    def backwards(self, orm):
        # Deleting model 'Route'
        db.delete_table('cartmanager_route')

        # Deleting model 'ServiceCenter'
        db.delete_table('cartmanager_servicecenter')

        # Deleting model 'ServiceCenterAddress'
        db.delete_table('cartmanager_servicecenteraddress')

        # Deleting model 'CollectionCustomer'
        db.delete_table('cartmanager_collectioncustomer')

        # Deleting model 'CollectionAddress'
        db.delete_table('cartmanager_collectionaddress')

        # Deleting model 'Cart'
        db.delete_table('cartmanager_cart')

        # Deleting model 'CartServiceTicket'
        db.delete_table('cartmanager_cartserviceticket')

        # Deleting model 'Users'
        db.delete_table('cartmanager_users')

        # Deleting model 'CartsUploadFile'
        db.delete_table('cartmanager_cartsuploadfile')

        # Deleting model 'TicketsCompleteUploadFile'
        db.delete_table('cartmanager_ticketscompleteuploadfile')

        # Deleting model 'CustomersUploadFile'
        db.delete_table('cartmanager_customersuploadfile')

        # Deleting model 'DataErrors'
        db.delete_table('cartmanager_dataerrors')


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
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'size': ('django.db.models.fields.IntegerField', [], {})
        },
        'cartmanager.cartserviceticket': {
            'Meta': {'ordering': "['-date_created']", 'object_name': 'CartServiceTicket'},
            'audit_status': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'broken_comments': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'broken_component': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'cart': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cartmanager.Cart']", 'null': 'True', 'blank': 'True'}),
            'cart_type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'date_completed': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_last_accessed': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'device_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '10', 'blank': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cartmanager.CollectionAddress']"}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '10', 'blank': 'True'}),
            'service_type': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
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
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
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
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
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
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"})
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
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
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
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"})
        },
        'cartmanager.route': {
            'Meta': {'object_name': 'Route'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'route': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'route_day': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'route_type': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"})
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
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
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
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
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