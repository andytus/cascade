__author__ = 'jbennett'

from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.contrib.sites.models import Site
from cascade.apps.cartmanager.models import CartsUploadFile, TicketsCompleteUploadFile, CustomersUploadFile, \
Cart, CartStatus, CartType, InventoryAddress, DataErrors

from datetime import datetime

def save_error(e, line):
    error_message = e.message
    print error_message
    if hasattr(e, 'message_dict'):
        for key, value in e.message_dict.iteritems():
            error_message += "%s: %s " % (str(key).upper(), ','.join(value))
    Site.objects.clear_cache()
    error = DataErrors(error_message=error_message, error_type = type(e), failed_data=line, site=Site.objects.get_current())
    error.save()




def save_cart_records(line, site):

    try:
        status = CartStatus.objects.get(label = 'Produced')
        rfid, serial, size, cart_type, born_date = line.split(',')
        # get cart type by name
        cart_type = CartType.objects.get(name=cart_type, size=size)
        cart = Cart(site=site, inventory_location = InventoryAddress.on_site.get(default=True),
            cart_type=cart_type, current_status=status, born_date=datetime.strptime(born_date.strip(), "%m/%d/%Y"))
        cart.full_clean()
        cart.save()

    except (Exception, ValidationError, ValueError, IntegrityError) as e:
        #self.status = "FAILED"
        #self.num_error +=1
        #save_error(e, line)
        pass




#    try:
#        # default status is produced
#        status = CartStatus.objects.get(label = 'Produced')

#        rfid, serial, size, cart_type, born_date = line.split(',')
#        # get cart type by name
#        cart_type = CartType.objects.get(name=cart_type, size=size)
#        cart = Cart(site=site, inventory_location = InventoryAddress.on_site.get(default=True),
#            updated_by = self.uploaded_by, rfid=rfid, serial_number=serial, size=size,
#            cart_type=cart_type, current_status=status,
#            born_date=datetime.strptime(born_date.strip(), "%m/%d/%Y"))
#
#        cart.full_clean()
#        cart.save()
#        self.num_good += 1
#    except (Exception, ValidationError, ValueError, IntegrityError) as e:
#        self.status = "FAILED"
#        self.num_error +=1
#        save_error(e, line)




def process_upload_records(file_model, site, file_id):
    file_record = file_model.objects.get(site=site, pk=file_id)
    file = file_record.file_path
    print file_record.file_path, "here"

    #Read use the first header row:
    file.readline()

    file_record.date_start_processing = datetime.now()

    while 1:
        lines = file.readlines(1000000)
        if not lines:
            break
        for line in lines:
            if file_record.file_kind == 'Cart':
                save_cart_records(line, site)



#def process(self, process):
#    """
#     Processes new uploaded files
#
#     Saves number of records, number of good and number of errors.
#     Saves status and processing time in seconds.
#
#    """
#    self.num_records = 0
#    self.num_good = 0
#    self.num_error = 0
#
#    #self.records_processed = process
#
#    file = self.file_path
#    # Read just the first header row:
#    file.readline()
#    self.status = 'UPLOADED'
#    self.date_start_processing = datetime.now()
#    while 1:
#        lines = file.readlines(1000000)
#        if not lines:
#            break
#        for line in lines:
#
#            self.save_records(line, self.site, self.records_processed)
#
#    self.num_records = self.num_good + self.num_error
#    self.date_end_processing = datetime.now()
#    self.total_process_time = (self.date_end_processing - self.date_start_processing).seconds
#    self.save()
#    self.file_path.close()
#    return self.num_records, self.num_good, self.num_error