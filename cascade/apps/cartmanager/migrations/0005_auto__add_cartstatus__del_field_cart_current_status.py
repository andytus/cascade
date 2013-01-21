# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CartStatus'
        db.create_table('cartmanager_cartstatus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('level', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=35)),
        ))
        db.send_create_signal('cartmanager', ['CartStatus'])

        # Deleting field 'Cart.current_status'
        db.delete_column('cartmanager_cart', 'current_status')


    def backwards(self, orm):
        # Deleting model 'CartStatus'
        db.delete_table('cartmanager_cartstatus')

        # Adding field 'Cart.current_status'
        db.add_column('cartmanager_cart', 'current_status',
                      self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True),
                      keep_default=False)


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'cartmanager.cart': {
            'Meta': {'object_name': 'Cart'},
            'born_date': ('django.db.models.fields.DateTimeField', [], {}),
            'cart_type': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
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
        'cartmanager.cartstatus': {
            'Meta': {'object_name': 'CartStatus'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '25'})
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
            'other_system_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
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
        'cartmanager.useraccountprofile': {
            'Meta': {'object_name': 'UserAccountProfile'},
            'company': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sites.Site']", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['cartmanager']