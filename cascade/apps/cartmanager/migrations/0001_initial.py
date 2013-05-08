# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AdminDefaults'
        db.create_table('cartmanager_admindefaults', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('account_admin', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
        ))
        db.send_create_signal('cartmanager', ['AdminDefaults'])

        # Adding model 'ZipCodes'
        db.create_table('cartmanager_zipcodes', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('zipcode', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('plus_four', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('defaults', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='default_zipcodes', null=True, to=orm['cartmanager.AdminDefaults'])),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
        ))
        db.send_create_signal('cartmanager', ['ZipCodes'])

        # Adding model 'CartStatus'
        db.create_table('cartmanager_cartstatus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('level', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
        ))
        db.send_create_signal('cartmanager', ['CartStatus'])

        # Adding model 'CartType'
        db.create_table('cartmanager_carttype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('size', self.gf('django.db.models.fields.IntegerField')()),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
        ))
        db.send_create_signal('cartmanager', ['CartType'])

        # Adding model 'TicketStatus'
        db.create_table('cartmanager_ticketstatus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('level', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('service_status', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
        ))
        db.send_create_signal('cartmanager', ['TicketStatus'])

        # Adding model 'CartServiceType'
        db.create_table('cartmanager_cartservicetype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('service', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=300, null=True)),
            ('complete_cart_status_change', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cartmanager.CartStatus'])),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
        ))
        db.send_create_signal('cartmanager', ['CartServiceType'])

        # Adding model 'ServiceReasonCodes'
        db.create_table('cartmanager_servicereasoncodes', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=300, null=True)),
        ))
        db.send_create_signal('cartmanager', ['ServiceReasonCodes'])

        # Adding model 'Route'
        db.create_table('cartmanager_route', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('route', self.gf('django.db.models.fields.CharField')(max_length=15, null=True)),
            ('route_day', self.gf('django.db.models.fields.CharField')(max_length=15, null=True)),
            ('route_type', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
        ))
        db.send_create_signal('cartmanager', ['Route'])

        # Adding model 'CollectionCustomer'
        db.create_table('cartmanager_collectioncustomer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(default='UNKNOWN', max_length=25, null=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(default='UNKNOWN', max_length=50, null=True)),
            ('phone_number', self.gf('django.contrib.localflavor.us.models.PhoneNumberField')(max_length=20, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
        ))
        db.send_create_signal('cartmanager', ['CollectionCustomer'])

        # Adding model 'ForeignSystemCustomerID'
        db.create_table('cartmanager_foreignsystemcustomerid', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('system_name', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('identity', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='customer', to=orm['cartmanager.CollectionCustomer'])),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=300, null=True, blank=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
        ))
        db.send_create_signal('cartmanager', ['ForeignSystemCustomerID'])

        # Adding model 'CollectionAddress'
        db.create_table('cartmanager_collectionaddress', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('house_number', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('street_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('unit', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(default='NA', max_length=25)),
            ('state', self.gf('django.db.models.fields.CharField')(default='NA', max_length=2)),
            ('zipcode', self.gf('django.db.models.fields.IntegerField')()),
            ('latitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=10, blank=True)),
            ('longitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=10, blank=True)),
            ('geocode_status', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('geocode_type', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('property_type', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('route', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cartmanager.Route'], null=True, blank=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='customer_location', null=True, to=orm['cartmanager.CollectionCustomer'])),
        ))
        db.send_create_signal('cartmanager', ['CollectionAddress'])

        # Adding unique constraint on 'CollectionAddress', fields ['house_number', 'street_name', 'unit']
        db.create_unique('cartmanager_collectionaddress', ['house_number', 'street_name', 'unit'])

        # Adding model 'InventoryAddress'
        db.create_table('cartmanager_inventoryaddress', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('house_number', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('street_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('unit', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(default='NA', max_length=25)),
            ('state', self.gf('django.db.models.fields.CharField')(default='NA', max_length=2)),
            ('zipcode', self.gf('django.db.models.fields.IntegerField')()),
            ('latitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=10, blank=True)),
            ('longitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=10, blank=True)),
            ('geocode_status', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('geocode_type', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('property_type', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('route', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cartmanager.Route'], null=True, blank=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
            ('contact_number', self.gf('django.contrib.localflavor.us.models.PhoneNumberField')(max_length=20, null=True, blank=True)),
            ('capacity', self.gf('django.db.models.fields.IntegerField')()),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=300, null=True, blank=True)),
            ('default', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('cartmanager', ['InventoryAddress'])

        # Adding unique constraint on 'InventoryAddress', fields ['house_number', 'street_name', 'unit']
        db.create_unique('cartmanager_inventoryaddress', ['house_number', 'street_name', 'unit'])

        # Adding model 'Cart'
        db.create_table('cartmanager_cart', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='location', null=True, to=orm['cartmanager.CollectionAddress'])),
            ('inventory_location', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='inventory_location', null=True, to=orm['cartmanager.InventoryAddress'])),
            ('last_latitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=10, blank=True)),
            ('last_longitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=10, blank=True)),
            ('rfid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('serial_number', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('size', self.gf('django.db.models.fields.IntegerField')()),
            ('current_status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cartmanager.CartStatus'], null=True, blank=True)),
            ('cart_type', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['cartmanager.CartType'], null=True, blank=True)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=datetime.datetime.now, blank=True)),
            ('born_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('updated_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='cart_updated_by_user', to=orm['auth.User'])),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
        ))
        db.send_create_signal('cartmanager', ['Cart'])

        # Adding model 'Ticket'
        db.create_table('cartmanager_ticket', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('serviced_cart', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='serviced_cart', null=True, to=orm['cartmanager.Cart'])),
            ('expected_cart', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='expected_cart', null=True, to=orm['cartmanager.Cart'])),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ticket_locations', to=orm['cartmanager.CollectionAddress'])),
            ('service_type', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='service_type', null=True, to=orm['cartmanager.CartServiceType'])),
            ('cart_type', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='cart_type', null=True, to=orm['cartmanager.CartType'])),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='status', null=True, to=orm['cartmanager.TicketStatus'])),
            ('date_completed', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('date_processed', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_last_attempted', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('latitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=10, blank=True)),
            ('longitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=10, blank=True)),
            ('device_name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('success_attempts', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('audit_status', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('broken_component', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('comments', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('reason_codes', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cartmanager.ServiceReasonCodes'], null=True, blank=True)),
            ('processed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='created_by_user', to=orm['auth.User'])),
            ('updated_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='updated_by_user', null=True, to=orm['auth.User'])),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
        ))
        db.send_create_signal('cartmanager', ['Ticket'])

        # Adding model 'UserAccountProfile'
        db.create_table('cartmanager_useraccountprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('company', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
        ))
        db.send_create_signal('cartmanager', ['UserAccountProfile'])

        # Adding M2M table for field sites on 'UserAccountProfile'
        db.create_table('cartmanager_useraccountprofile_sites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('useraccountprofile', models.ForeignKey(orm['cartmanager.useraccountprofile'], null=False)),
            ('site', models.ForeignKey(orm['sites.site'], null=False))
        ))
        db.create_unique('cartmanager_useraccountprofile_sites', ['useraccountprofile_id', 'site_id'])

        # Adding model 'CartsUploadFile'
        db.create_table('cartmanager_cartsuploadfile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file_path', self.gf('django.db.models.fields.files.FileField')(max_length=300)),
            ('uploaded_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
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
            ('records_processed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
        ))
        db.send_create_signal('cartmanager', ['CartsUploadFile'])

        # Adding model 'TicketsCompleteUploadFile'
        db.create_table('cartmanager_ticketscompleteuploadfile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file_path', self.gf('django.db.models.fields.files.FileField')(max_length=300)),
            ('uploaded_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
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
            ('records_processed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
            ('success_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('removal_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('audit_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('adhoc_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('unsucessful', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('repair_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('cartmanager', ['TicketsCompleteUploadFile'])

        # Adding model 'CustomersUploadFile'
        db.create_table('cartmanager_customersuploadfile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file_path', self.gf('django.db.models.fields.files.FileField')(max_length=300)),
            ('uploaded_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
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
            ('records_processed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
        ))
        db.send_create_signal('cartmanager', ['CustomersUploadFile'])

        # Adding model 'DataErrors'
        db.create_table('cartmanager_dataerrors', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('error_message', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('error_type', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('failed_data', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('error_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('fix_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
        ))
        db.send_create_signal('cartmanager', ['DataErrors'])


    def backwards(self, orm):
        # Removing unique constraint on 'InventoryAddress', fields ['house_number', 'street_name', 'unit']
        db.delete_unique('cartmanager_inventoryaddress', ['house_number', 'street_name', 'unit'])

        # Removing unique constraint on 'CollectionAddress', fields ['house_number', 'street_name', 'unit']
        db.delete_unique('cartmanager_collectionaddress', ['house_number', 'street_name', 'unit'])

        # Deleting model 'AdminDefaults'
        db.delete_table('cartmanager_admindefaults')

        # Deleting model 'ZipCodes'
        db.delete_table('cartmanager_zipcodes')

        # Deleting model 'CartStatus'
        db.delete_table('cartmanager_cartstatus')

        # Deleting model 'CartType'
        db.delete_table('cartmanager_carttype')

        # Deleting model 'TicketStatus'
        db.delete_table('cartmanager_ticketstatus')

        # Deleting model 'CartServiceType'
        db.delete_table('cartmanager_cartservicetype')

        # Deleting model 'ServiceReasonCodes'
        db.delete_table('cartmanager_servicereasoncodes')

        # Deleting model 'Route'
        db.delete_table('cartmanager_route')

        # Deleting model 'CollectionCustomer'
        db.delete_table('cartmanager_collectioncustomer')

        # Deleting model 'ForeignSystemCustomerID'
        db.delete_table('cartmanager_foreignsystemcustomerid')

        # Deleting model 'CollectionAddress'
        db.delete_table('cartmanager_collectionaddress')

        # Deleting model 'InventoryAddress'
        db.delete_table('cartmanager_inventoryaddress')

        # Deleting model 'Cart'
        db.delete_table('cartmanager_cart')

        # Deleting model 'Ticket'
        db.delete_table('cartmanager_ticket')

        # Deleting model 'UserAccountProfile'
        db.delete_table('cartmanager_useraccountprofile')

        # Removing M2M table for field sites on 'UserAccountProfile'
        db.delete_table('cartmanager_useraccountprofile_sites')

        # Deleting model 'CartsUploadFile'
        db.delete_table('cartmanager_cartsuploadfile')

        # Deleting model 'TicketsCompleteUploadFile'
        db.delete_table('cartmanager_ticketscompleteuploadfile')

        # Deleting model 'CustomersUploadFile'
        db.delete_table('cartmanager_customersuploadfile')

        # Deleting model 'DataErrors'
        db.delete_table('cartmanager_dataerrors')


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
        'cartmanager.admindefaults': {
            'Meta': {'object_name': 'AdminDefaults'},
            'account_admin': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'})
        },
        'cartmanager.cart': {
            'Meta': {'object_name': 'Cart'},
            'born_date': ('django.db.models.fields.DateTimeField', [], {}),
            'cart_type': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['cartmanager.CartType']", 'null': 'True', 'blank': 'True'}),
            'current_status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cartmanager.CartStatus']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inventory_location': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'inventory_location'", 'null': 'True', 'to': "orm['cartmanager.InventoryAddress']"}),
            'last_latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '10', 'blank': 'True'}),
            'last_longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '10', 'blank': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'datetime.datetime.now', 'blank': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'location'", 'null': 'True', 'to': "orm['cartmanager.CollectionAddress']"}),
            'rfid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'serial_number': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'size': ('django.db.models.fields.IntegerField', [], {}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cart_updated_by_user'", 'to': "orm['auth.User']"})
        },
        'cartmanager.cartservicetype': {
            'Meta': {'object_name': 'CartServiceType'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'complete_cart_status_change': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cartmanager.CartStatus']"}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '300', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'service': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"})
        },
        'cartmanager.cartstatus': {
            'Meta': {'object_name': 'CartStatus'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"})
        },
        'cartmanager.cartsuploadfile': {
            'Meta': {'object_name': 'CartsUploadFile'},
            'date_end_processing': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_start_processing': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_uploaded': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'file_kind': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'file_path': ('django.db.models.fields.files.FileField', [], {'max_length': '300'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'num_error': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'num_good': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'num_records': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'records_processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'size': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'PENDING'", 'max_length': '64'}),
            'total_process_time': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'uploaded_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'cartmanager.carttype': {
            'Meta': {'ordering': "['-name', '-size']", 'object_name': 'CartType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'size': ('django.db.models.fields.IntegerField', [], {})
        },
        'cartmanager.collectionaddress': {
            'Meta': {'unique_together': "(('house_number', 'street_name', 'unit'),)", 'object_name': 'CollectionAddress'},
            'city': ('django.db.models.fields.CharField', [], {'default': "'NA'", 'max_length': '25'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'customer_location'", 'null': 'True', 'to': "orm['cartmanager.CollectionCustomer']"}),
            'geocode_status': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'geocode_type': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'house_number': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '10', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '10', 'blank': 'True'}),
            'property_type': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'route': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cartmanager.Route']", 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'NA'", 'max_length': '2'}),
            'street_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'zipcode': ('django.db.models.fields.IntegerField', [], {})
        },
        'cartmanager.collectioncustomer': {
            'Meta': {'object_name': 'CollectionCustomer'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'default': "'UNKNOWN'", 'max_length': '25', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'default': "'UNKNOWN'", 'max_length': '50', 'null': 'True'}),
            'phone_number': ('django.contrib.localflavor.us.models.PhoneNumberField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"})
        },
        'cartmanager.customersuploadfile': {
            'Meta': {'object_name': 'CustomersUploadFile'},
            'date_end_processing': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_start_processing': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_uploaded': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'file_kind': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'file_path': ('django.db.models.fields.files.FileField', [], {'max_length': '300'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'num_error': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'num_good': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'num_records': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'records_processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'size': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'PENDING'", 'max_length': '64'}),
            'total_process_time': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'uploaded_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'cartmanager.dataerrors': {
            'Meta': {'ordering': "['-error_date']", 'object_name': 'DataErrors'},
            'error_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'error_message': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'error_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'failed_data': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'fix_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"})
        },
        'cartmanager.foreignsystemcustomerid': {
            'Meta': {'object_name': 'ForeignSystemCustomerID'},
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'customer'", 'to': "orm['cartmanager.CollectionCustomer']"}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identity': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'system_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'})
        },
        'cartmanager.inventoryaddress': {
            'Meta': {'unique_together': "(('house_number', 'street_name', 'unit'),)", 'object_name': 'InventoryAddress'},
            'capacity': ('django.db.models.fields.IntegerField', [], {}),
            'city': ('django.db.models.fields.CharField', [], {'default': "'NA'", 'max_length': '25'}),
            'contact_number': ('django.contrib.localflavor.us.models.PhoneNumberField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'geocode_status': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'geocode_type': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'house_number': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '10', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '10', 'blank': 'True'}),
            'property_type': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'route': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cartmanager.Route']", 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'NA'", 'max_length': '2'}),
            'street_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'zipcode': ('django.db.models.fields.IntegerField', [], {})
        },
        'cartmanager.route': {
            'Meta': {'object_name': 'Route'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'route': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'route_day': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'route_type': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"})
        },
        'cartmanager.servicereasoncodes': {
            'Meta': {'object_name': 'ServiceReasonCodes'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '300', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'cartmanager.ticket': {
            'Meta': {'ordering': "['-date_created']", 'object_name': 'Ticket'},
            'audit_status': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'broken_component': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'cart_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'cart_type'", 'null': 'True', 'to': "orm['cartmanager.CartType']"}),
            'comments': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'created_by_user'", 'to': "orm['auth.User']"}),
            'date_completed': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_last_attempted': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'date_processed': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'device_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'expected_cart': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'expected_cart'", 'null': 'True', 'to': "orm['cartmanager.Cart']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '10', 'blank': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ticket_locations'", 'to': "orm['cartmanager.CollectionAddress']"}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '10', 'blank': 'True'}),
            'processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reason_codes': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cartmanager.ServiceReasonCodes']", 'null': 'True', 'blank': 'True'}),
            'service_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'service_type'", 'null': 'True', 'to': "orm['cartmanager.CartServiceType']"}),
            'serviced_cart': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'serviced_cart'", 'null': 'True', 'to': "orm['cartmanager.Cart']"}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'status'", 'null': 'True', 'to': "orm['cartmanager.TicketStatus']"}),
            'success_attempts': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'updated_by_user'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'cartmanager.ticketscompleteuploadfile': {
            'Meta': {'object_name': 'TicketsCompleteUploadFile'},
            'adhoc_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'audit_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'date_end_processing': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_start_processing': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'date_uploaded': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'file_kind': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'file_path': ('django.db.models.fields.files.FileField', [], {'max_length': '300'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'num_error': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'num_good': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'num_records': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'records_processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'removal_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'repair_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'size': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'PENDING'", 'max_length': '64'}),
            'success_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'total_process_time': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'unsucessful': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'uploaded_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'cartmanager.ticketstatus': {
            'Meta': {'object_name': 'TicketStatus'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'service_status': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"})
        },
        'cartmanager.useraccountprofile': {
            'Meta': {'object_name': 'UserAccountProfile'},
            'company': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sites.Site']", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'cartmanager.zipcodes': {
            'Meta': {'object_name': 'ZipCodes'},
            'defaults': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'default_zipcodes'", 'null': 'True', 'to': "orm['cartmanager.AdminDefaults']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'plus_four': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '5'})
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