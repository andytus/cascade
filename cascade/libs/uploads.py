__author__ = 'jbennett'

from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.contrib.sites.models import Site
from django.db import transaction
from cascade.apps.cartmanager.models import Cart, CartStatus, CartType, InventoryAddress, DataErrors, Ticket, \
    TicketStatus, TicketComments, CollectionCustomer, CartServiceType, \
    CollectionAddress, ForeignSystemCustomerID, ServiceReasonCodes, Route
from django.utils import timezone
from datetime import datetime


def save_error(e, line):
    error_message = e.message
    if hasattr(e, 'message_dict'):
        for key, value in e.message_dict.iteritems():
            error_message += "%s: %s " % (str(key).upper(), ','.join(value))
    Site.objects.clear_cache()
    error = DataErrors(error_message=error_message, error_type=type(e),
                       failed_data=line, site=Site.objects.get_current())
    error.save()


def save_cart_records(line, file_record):
    try:
        rfid, serial, size, cart_type, born_date, status, house, street, unit = line.split(',')
        # get cart type by name
        cart_type = CartType.objects.get(name=cart_type, size=size)
        cart_status = CartStatus.objects.get(label=status)
        cart = Cart(site=file_record.site, rfid=rfid, updated_by=file_record.uploaded_by, serial_number=serial,
                    size=size, inventory_location=InventoryAddress.objects.get(site=file_record.site, default=True),
                    file_upload=file_record,cart_type=cart_type, current_status=cart_status,
                    born_date=datetime.strptime(born_date.strip(), "%m/%d/%Y"))
        #TODO work on getting unit logic
        try:
            if status == 'Delivered':
                location = CollectionAddress.objects.get(site=file_record.site,
                                                         house_number=house.strip(), street_name=street)
                if location:
                    cart.location = location
                    cart.at_inventory = False
            else:
                cart.at_inventory = True
        except Exception as e:
            #cant find put the cart in inventory
            cart.at_inventory = True

        cart.full_clean()
        cart.save()
        file_record.num_good += 1

    except (Exception, ValidationError, ValueError, IntegrityError) as e:
        file_record.status = "FAILED"
        file_record.num_error +=1
        save_error(e, line)


def save_ticket_records(line, file_record):
    try:
        # Get imported files data
        # TODO Change names to actual headers: SystemID,StreetName,HouseNumber,UnitNumber,ServiceType,
        # TODO..  RFID, ContainerSize, ContainerType, TicketStatus,DateTime,UserName,Latitude,Longitude,
        # TODO.. BrokenComponent,Comments
        system_id, street, house_number, unit_number, service_type, rfid, container_size, container_type, \
            upload_ticket_status, complete_datetime, device_name, lat, lon, broken_component, comment = line.split(',')

        ticket = Ticket.on_site.get(pk=system_id)
         #matches time as 11/1/2012 15:20
        time_format = '%m/%d/%Y %H:%M:%S'

        #get or create cart
        if len(rfid) > 4:
            print "in rfid check"
            try:
                clean_rifd = rfid.strip('=').strip('"')
                cart = Cart.on_site.get(rfid__exact=clean_rifd)
            except Cart.DoesNotExist:
                cart = Cart(site=file_record.site, rfid=clean_rifd,
                            serial_number=rfid.strip('=').strip('"')[-8:],
                            size=container_size, updated_by=file_record.uploaded_by)
            cart.save()

        # check for status uploaded or complete, because you don't want to over write already completed tickets.
        if ticket.status.service_status != 'Completed':
            if lat and type(lat) == float:
                ticket.latitude = lat
                ticket.longitude = lon
            if comment.strip() and type(comment) is str:
                ticket_comment = TicketComments(site=file_record.site, text=comment +
                                                " -Imported from reader device: %s" % device_name,
                                                ticket=ticket, created_by=file_record.uploaded_by)
                ticket_comment.save()
                #status from the uploaded file
            if ticket.service_type.code == 'REPAIR':
                file_record.repair_count += 1
                ticket.success_attempts += 1
                ticket.date_completed = datetime.strptime(complete_datetime.strip(), time_format)
                ticket.serviced_cart = cart

            elif upload_ticket_status.split("-")[0] == "UNSUCCESSFUL":
                if "-" in upload_ticket_status:
                    ticket.reason_codes = ServiceReasonCodes.objects.get(description=upload_ticket_status.split("-")[1])
                file_record.unsuccessful += 1
                ticket.success_attempts += 1
                ticket.date_last_attempted = datetime.strptime(complete_datetime.strip(), time_format)
                ticket.status = TicketStatus.on_site.get(site=file_record.site, service_status='Unsuccessful')
                print "end of unsuccessful"

            elif upload_ticket_status == 'COMPLETED':
                print "in completed"
                ticket.updated_by = file_record.uploaded_by
                file_record.success_count += 1
                ticket.success_attempts += 1
                ticket.serviced_cart = cart

                #goes into  cart processing here
                #grab cart from the serviced cart
                cart_type_update = CartType.on_site.get(name=container_type, size=container_size)
                cart.cart_type = cart_type_update
                ticket.status = TicketStatus.on_site.get(service_status='Completed')
                print ticket.status
                ticket.date_completed = datetime.strptime(complete_datetime.strip(), time_format)
                ticket.processed = True
                #updating current cart status
                cart.current_status = ticket.service_type.complete_cart_status_change

                if ticket.service_type.code == 'DEL' or ticket.service_type.code == 'EX-DEL':
                    cart.location = ticket.location
                    #set to not at inventory
                    cart.at_inventory = False
                    #check if latitude was updated
                    if ticket.latitude:
                        cart.last_latitude = ticket.latitude
                        cart.last_longitude = ticket.longitude

                elif ticket.service_type.code == "EX-REM" or ticket.service_type.code == "REM":
                    # check to see if the expected cart is the same as the serviced cart
                    # In other words, did the correct cart get removed
                    if ticket.expected_cart == ticket.serviced_cart:
                        # check to see if the removed cart is still at the ticket location before removing
                        # because it could have been delivered to another addresss
                        if ticket.location == cart.location:
                            #remove location from serviced cart and put in inventory
                            cart.location = None
                            #set inventory location
                            cart.inventory_location = InventoryAddress.on_site.get(default=True)
                            cart.at_inventory = True
                            cart.last_latitude = cart.inventory_location.latitude
                            cart.last_longitude = cart.inventory_location.longitude

                    else:
                    # else ticket.expected is not equal to ticket.serviced (i.e. picked up the wrong cart)
                    # Check if last update is greater than or equal to 2 days and update location to None
                    # else it has been updated, and most likely it has been processed
                    # as a delivery today, leave it alone.
                        print "in day check wrong Cart"
                        days_last_updated = (timezone.now() - cart.last_updated).days
                        if days_last_updated >= 2:
                            cart.location = None
                            cart.inventory_location = InventoryAddress.on_site.get(default=True)
                            cart.at_inventory = True
                            cart.last_latitude = cart.inventory_location.latitude
                            cart.last_longitude = cart.inventory_location.longitude
                            #cart.current_status = ticket.service_type.complete_cart_status_change
                cart.save()
            ticket.save()
            file_record.num_good += 1

    except (Exception, ValidationError, ValueError, IntegrityError) as e:
        print e
        file_record.status = "FAILED"
        file_record.num_error += 1
        error_message = e.message
        if hasattr(e, 'message_dict'):
            for key, value in e.message_dict.iteritems():
                error_message += "%s: %s " % (str(key).upper(), ','.join(value))
        error = DataErrors(site=file_record.site, error_message=error_message, error_type=type(e), failed_data=line)
        error.save()


def save_customer_records(line, file_record):
    try:
        #Customer setup & save:
        systemid, system_name, first_name, last_name, phone, email, house_number, street_name, unit, city,\
        state, zipcode, property_type, latitude, longitude, recycle, recycle_size, refuse, refuse_size, yard_organics,\
        yard_organics_size, unassigned, unassigned_size, refuse_route, refuse_route_day,\
        recycle_route, recycle_route_day, yard_organics_route, yard_organics_route_day = line.split(',')

        customer = CollectionCustomer(site=file_record.site, first_name=first_name[:25].upper(),
                                      last_name=last_name[:50].upper(), email=email, phone_number=phone)


        #full_clean checks for the correct data
        customer.full_clean()
        customer.save()

        # systemid should be zero as default if not used
        # saves ForeignSystemCustomerID and assigns to customer, customer can have multiple ids but id can not
        # belong to multiple customers
        if systemid:
            new_foreign_system_id = ForeignSystemCustomerID(identity=systemid, customer=customer,
                                                            system_name=system_name, site=file_record.site)
            new_foreign_system_id.save()

        # Collection_Address setup & save:
        collection_address = CollectionAddress(site=file_record.site, customer=customer,
                                               house_number=house_number.strip(),
                                               street_name=street_name.strip().upper(), unit=unit.strip(),
                                               city=city, zipcode=zipcode, state=state, latitude=latitude,
                                               longitude=longitude, property_type=property_type)

        collection_address.full_clean()
        collection_address.save()

        refuse_address_route = None
        recycle_address_route = None
        yard_organics_address_route = None

        if refuse_route != 'Null':

            refuse_address_route, created = Route.on_site.get_or_create(site=file_record.site, route=refuse_route,
                                                                        route_day=refuse_route_day,
                                                                        defaults={'route_type': 'Refuse'})
            collection_address.route.add(refuse_address_route)

        if recycle_route != 'Null':

            recycle_address_route, created = Route.on_site.get_or_create(site=file_record.site, route=recycle_route,
                                                                         route_day=recycle_route_day,
                                                                         defaults={'route_type': 'Recycle'})
            collection_address.route.add(recycle_address_route)

        if yard_organics_route != 'Null':

            yard_organics_address_route, created = Route.on_site.get_or_create(site=file_record.site,
                                                                               route=yard_organics_route,
                                                                               route_day=yard_organics_route_day,
                                                                            defaults={'route_type': 'Yard & Organic'})
            collection_address.route.add(yard_organics_address_route)


        # Tickets setup & save for Refuse, Recycle, Other, Yard\Organics:
        delivery = CartServiceType.on_site.get(site=file_record.site, code="DEL")
        requested = TicketStatus.on_site.get(site=file_record.site, service_status="Requested")
        user = file_record.uploaded_by

        if refuse.isdigit():
            for x in range(int(refuse)):
                t = Ticket(cart_type=CartType.on_site.get(site=file_record.site, name="Refuse", size=int(refuse_size)),
                           service_type=delivery, location=collection_address, status=requested, created_by=user)
                if refuse_address_route:
                    t.route = refuse_address_route
                t.save()

        if recycle.isdigit():
            for x in range(int(recycle)):
                t = Ticket(cart_type=CartType.on_site.get(site=file_record.site, name="Recycle", size=int(recycle_size))
                           , service_type=delivery, location=collection_address, status=requested, created_by=user)
                if recycle_address_route:
                    t.route = recycle_address_route
                t.save()

        if yard_organics.isdigit():
            for x in range(int(yard_organics)):
                t = Ticket(cart_type=CartType.on_site.get(site=file_record.site, name="Yard",
                                                          size=int(yard_organics_size)), service_type=delivery,
                                                           location=collection_address, status=requested,
                                                           created_by=user)
                if yard_organics_address_route:
                    t.route = yard_organics_address_route
                t.save()

        #Used for unassigned type carts
        if unassigned.isdigit():
            for x in range(int(unassigned)):
                Ticket(cart_type=CartType.on_site.get(site=file_record.site, name="Unassigned",
                                                      size=int(unassigned_size)), service_type=delivery,
                       location=collection_address, status=requested, created_by=user).save()

        file_record.num_good += 1

    except Exception as e:
        file_record.status = "FAILED"
        file_record.num_error += 1
        error = DataErrors(site=file_record.site, error_message=e, error_type=type(e), failed_data=line)
        error.save()


def save_route_records(line, file_record):
    try:
        route, route_day, route_type, house_number, street_name, unit = line.split(',')
        route, created = Route.on_site.get_or_create(site=file_record.site, route=route,
                                                     route_day=route_day, route_type=route_type)
        if unit.strip():
            print "in unit"
            collection_address = CollectionAddress.objects.get(house_number=house_number,
                                                               street_name=street_name.strip().upper(),
                                                               unit=unit.strip())
        else:
            collection_address = CollectionAddress.objects.get(house_number=house_number,
                                                               street_name=street_name.strip().upper())
        collection_address.route.add(route)

        route.save()
        file_record.num_good += 1

    except Exception as e:
        file_record.status = "FAILED"
        file_record.num_error += 1
        error = DataErrors(site=file_record.site, error_message=e, error_type=type(e), failed_data=line)
        error.save()


def process_upload_records(file_model, file_id):
    file_record = file_model.objects.get(pk=file_id)
    file = file_record.file_path
    #Read use the first header row:
    file.readline()
    #Timer started
    file_record.date_start_processing = datetime.now()

    while 1:
        lines = file.readlines(1000000)
        if not lines:
            break
        for line in lines:
            if file_record.file_kind == 'Carts':
                save_cart_records(line, file_record)
            elif file_record.file_kind == 'Tickets':
                save_ticket_records(line, file_record)
            elif file_record.file_kind == 'Customers':
                save_customer_records(line, file_record)
            elif file_record.file_kind == 'Route':
                save_route_records(line, file_record)

    file_record.num_records = file_record.num_good + file_record.num_error
    file_record.date_end_processing = datetime.now()
    file_record.total_process_time = (file_record.date_end_processing - file_record.date_start_processing).seconds
    file_record.save()
    file_record.file_path.close()
    file_record.save()