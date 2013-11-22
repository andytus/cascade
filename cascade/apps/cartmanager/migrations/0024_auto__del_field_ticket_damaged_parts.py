# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Ticket.damaged_parts'
        db.delete_column(u'cartmanager_ticket', 'damaged_parts_id')

        # Adding M2M table for field damaged_parts on 'Ticket'
        db.create_table(u'cartmanager_ticket_damaged_parts', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('ticket', models.ForeignKey(orm[u'cartmanager.ticket'], null=False)),
            ('cartparts', models.ForeignKey(orm[u'cartmanager.cartparts'], null=False))
        ))
        db.create_unique(u'cartmanager_ticket_damaged_parts', ['ticket_id', 'cartparts_id'])


    def backwards(self, orm):
        # Adding field 'Ticket.damaged_parts'
        db.add_column(u'cartmanager_ticket', 'damaged_parts',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='damaged_parts', null=True, to=orm['cartmanager.CartParts'], blank=True),
                      keep_default=False)

        # Removing M2M table for field damaged_parts on 'Ticket'
        db.delete_table('cartmanager_ticket_damaged_parts')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'cartmanager.admindefaults': {
            'Meta': {'object_name': 'AdminDefaults'},
            'account_admin': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'})
        },
        u'cartmanager.cart': {
            'Meta': {'object_name': 'Cart'},
            'at_inventory': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'born_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'cart_type': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['cartmanager.CartType']", 'null': 'True', 'blank': 'True'}),
            'current_status': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cartmanager.CartStatus']", 'null': 'True', 'blank': 'True'}),
            'file_upload': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'cart_upload_file'", 'null': 'True', 'to': u"orm['cartmanager.CartsUploadFile']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inventory_location': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'inventory_location'", 'null': 'True', 'to': u"orm['cartmanager.InventoryAddress']"}),
            'last_latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '10', 'blank': 'True'}),
            'last_longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '10', 'blank': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'datetime.datetime.now', 'blank': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'location'", 'null': 'True', 'to': u"orm['cartmanager.CollectionAddress']"}),
            'rfid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'serial_number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cart_updated_by_user'", 'to': u"orm['auth.User']"})
        },
        u'cartmanager.cartparts': {
            'Meta': {'object_name': 'CartParts'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'on_hand': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['sites.Site']", 'symmetrical': 'False'})
        },
        u'cartmanager.cartservicecharge': {
            'Meta': {'object_name': 'CartServiceCharge'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'currency': ('django.db.models.fields.CharField', [], {'default': "'US Dollars'", 'max_length': '50'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '120', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['sites.Site']", 'symmetrical': 'False'})
        },
        u'cartmanager.cartservicetype': {
            'Meta': {'object_name': 'CartServiceType'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'complete_cart_status_change': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cartmanager.CartStatus']"}),
            'default_charge': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'default_charge'", 'null': 'True', 'to': u"orm['cartmanager.CartServiceCharge']"}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '300', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'service': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'site': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['sites.Site']", 'symmetrical': 'False'})
        },
        u'cartmanager.cartstatus': {
            'Meta': {'object_name': 'CartStatus'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'site': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['sites.Site']", 'symmetrical': 'False'})
        },
        u'cartmanager.cartsuploadfile': {
            'Meta': {'object_name': 'CartsUploadFile'},
            'date_end_processing': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_start_processing': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_uploaded': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'file_kind': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'file_path': ('django.db.models.fields.files.FileField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'num_error': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'num_good': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'num_records': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'records_processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'size': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'PENDING'", 'max_length': '64'}),
            'total_process_time': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'uploaded_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'cartmanager.carttype': {
            'Meta': {'ordering': "['-name', '-size']", 'object_name': 'CartType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'site': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['sites.Site']", 'symmetrical': 'False'}),
            'size': ('django.db.models.fields.IntegerField', [], {})
        },
        u'cartmanager.collectionaddress': {
            'Meta': {'unique_together': "(('house_number', 'street_name', 'unit'),)", 'object_name': 'CollectionAddress'},
            'city': ('django.db.models.fields.CharField', [], {'default': "'NA'", 'max_length': '25'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'customer_location'", 'null': 'True', 'to': u"orm['cartmanager.CollectionCustomer']"}),
            'geocode_status': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'geocode_type': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'house_number': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '10', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '10', 'blank': 'True'}),
            'property_type': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'route': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['cartmanager.Route']", 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'NA'", 'max_length': '2'}),
            'street_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'zipcode': ('django.db.models.fields.IntegerField', [], {})
        },
        u'cartmanager.collectioncustomer': {
            'Meta': {'object_name': 'CollectionCustomer'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'file_upload': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'customers_upload_file'", 'null': 'True', 'to': u"orm['cartmanager.CustomersUploadFile']"}),
            'first_name': ('django.db.models.fields.CharField', [], {'default': "'UNKNOWN'", 'max_length': '25', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'default': "'UNKNOWN'", 'max_length': '50', 'null': 'True'}),
            'phone_number': ('django.contrib.localflavor.us.models.PhoneNumberField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"})
        },
        u'cartmanager.customersuploadfile': {
            'Meta': {'object_name': 'CustomersUploadFile'},
            'date_end_processing': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_start_processing': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_uploaded': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'file_kind': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'file_path': ('django.db.models.fields.files.FileField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'num_error': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'num_good': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'num_records': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'records_processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'size': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'PENDING'", 'max_length': '64'}),
            'total_process_time': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'uploaded_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'cartmanager.dataerrors': {
            'Meta': {'ordering': "['-error_date']", 'object_name': 'DataErrors'},
            'error_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'error_message': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'error_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'failed_data': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'fix_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"})
        },
        u'cartmanager.foreignsystemcustomerid': {
            'Meta': {'object_name': 'ForeignSystemCustomerID'},
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'customer'", 'to': u"orm['cartmanager.CollectionCustomer']"}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identity': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'system_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'})
        },
        u'cartmanager.inventoryaddress': {
            'Meta': {'object_name': 'InventoryAddress'},
            'capacity': ('django.db.models.fields.IntegerField', [], {}),
            'city': ('django.db.models.fields.CharField', [], {'default': "'NA'", 'max_length': '25'}),
            'contact_number': ('django.contrib.localflavor.us.models.PhoneNumberField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'geocode_status': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'geocode_type': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'house_number': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '10', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '10', 'blank': 'True'}),
            'property_type': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'route': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['cartmanager.Route']", 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'NA'", 'max_length': '2'}),
            'street_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'zipcode': ('django.db.models.fields.IntegerField', [], {})
        },
        u'cartmanager.route': {
            'Meta': {'object_name': 'Route'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'route': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'route_day': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'route_type': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"})
        },
        u'cartmanager.routeuploadfile': {
            'Meta': {'object_name': 'RouteUploadFile'},
            'date_end_processing': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_start_processing': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_uploaded': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'file_kind': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'file_path': ('django.db.models.fields.files.FileField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'num_error': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'num_good': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'num_records': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'records_processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'size': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'PENDING'", 'max_length': '64'}),
            'total_process_time': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'uploaded_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'cartmanager.servicereasoncodes': {
            'Meta': {'object_name': 'ServiceReasonCodes'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '300', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'cartmanager.ticket': {
            'Meta': {'ordering': "['-date_created']", 'object_name': 'Ticket'},
            'audit_status': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'cart_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'cart_type'", 'null': 'True', 'to': u"orm['cartmanager.CartType']"}),
            'charge': ('django.db.models.fields.DecimalField', [], {'default': '0.0', 'max_digits': '10', 'decimal_places': '2'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'created_by_user'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'damaged_parts': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'damaged_parts'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['cartmanager.CartParts']"}),
            'date_completed': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_last_attempted': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'date_processed': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'device_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'expected_cart': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'expected_cart'", 'null': 'True', 'to': u"orm['cartmanager.Cart']"}),
            'file_upload': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tickets_upload_file'", 'null': 'True', 'to': u"orm['cartmanager.TicketsCompleteUploadFile']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '10', 'blank': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ticket_locations'", 'to': u"orm['cartmanager.CollectionAddress']"}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '10', 'blank': 'True'}),
            'processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reason_codes': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cartmanager.ServiceReasonCodes']", 'null': 'True', 'blank': 'True'}),
            'route': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'ticket_route'", 'null': 'True', 'to': u"orm['cartmanager.Route']"}),
            'service_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'service_type'", 'null': 'True', 'to': u"orm['cartmanager.CartServiceType']"}),
            'serviced_cart': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'serviced_cart'", 'null': 'True', 'to': u"orm['cartmanager.Cart']"}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'status'", 'null': 'True', 'to': u"orm['cartmanager.TicketStatus']"}),
            'success_attempts': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'updated_by_user'", 'null': 'True', 'to': u"orm['auth.User']"})
        },
        u'cartmanager.ticketcomments': {
            'Meta': {'object_name': 'TicketComments'},
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'created_by'", 'blank': 'True', 'to': u"orm['auth.User']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'text': ('django.db.models.fields.TextField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'ticket': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ticket_comment'", 'to': u"orm['cartmanager.Ticket']"})
        },
        u'cartmanager.ticketscompleteuploadfile': {
            'Meta': {'object_name': 'TicketsCompleteUploadFile'},
            'adhoc_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'audit_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'date_end_processing': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_start_processing': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_uploaded': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'file_kind': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'file_path': ('django.db.models.fields.files.FileField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'num_error': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'num_good': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'num_records': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'records_processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'removal_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'repair_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'size': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'PENDING'", 'max_length': '64'}),
            'success_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'total_process_time': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'unsuccessful': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'uploaded_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'cartmanager.ticketstatus': {
            'Meta': {'object_name': 'TicketStatus'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'service_status': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'site': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['sites.Site']", 'symmetrical': 'False'})
        },
        u'cartmanager.useraccountprofile': {
            'Meta': {'object_name': 'UserAccountProfile'},
            'company': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['sites.Site']", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'cartmanager.zipcodes': {
            'Meta': {'object_name': 'ZipCodes'},
            'defaults': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'default_zipcodes'", 'null': 'True', 'to': u"orm['cartmanager.AdminDefaults']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'plus_four': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['cartmanager']