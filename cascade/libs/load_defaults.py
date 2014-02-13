__author__ = 'jbennett'

from django.contrib.sites.models import Site
from cascade.apps.cartmanager.models import CartStatus, CartType, TicketStatus, CartServiceType, ServiceReasonCodes


class LoadData:

    def __init__(self):
        self.default_site = 2
        self.cart_types = [{'name': 'Trash', 'size': 96},
                           {'name': 'Trash', 'size': 64},
                           {'name': 'Trash', 'size': 35},
                           {'name': 'Recycle', 'size': 96},
                           {'name': 'Recycle', 'size': 64},
                           {'name': 'Recycle', 'size': 35}
                           ]
        self.service_types = [{'service': 'Exchange Remove', 'code': 'EX-REM', 'description': 'Exchange Remove',
                                'complete_cart_status_change':'Inventory'},
                                {'service': 'Exchange Delivery', 'code': 'EX-DEL', 'description': 'Exchange Remove',
                                'complete_cart_status_change':'Delivered'},
                                {'service': 'Delivery', 'code': 'DEL', 'description': 'Delivery',
                                'complete_cart_status_change':'Delivered'},
                                {'service': 'Remove', 'code': 'REM', 'description': 'Remove',
                                'complete_cart_status_change': 'Inventory'},
                              ]

        self.cart_status = [{'level': 'Default', 'label': 'Repaired'},
                            {'level': 'Info', 'label': 'Inventory'},
                            {'level': 'Damaged', 'label': 'Damaged'},
                            {'level': 'Warning', 'label': 'Lost'},
                            {'level': 'Success', 'label': 'Delivered'}
                            ]
        self.ticket_status = [{'level': 'Info', 'service_status': 'Requested'},
                              {'level': 'Completed', 'service_status': 'Success'},
                              {'level': 'Alert', 'service_status': 'Unsuccessful'},
                              {'level': 'Info', 'service_status': 'Uploaded'},
                              ]

        self.reason_codes = [{'code': 'Vacant Lot', 'description': 'Vacant Lot'},
                             {'code': 'Unoccupied', 'description': 'Unoccupied'},
                             {'code': 'Owner Refused', 'description': 'Owner Refused'},
                             {'code': 'Data Error', 'description': 'Data Error'},
                             {'code': 'Commercial', 'description': 'Commercial'},
                             {'code': 'Cannot Find Address', 'description': 'Cannot Find Address'}]

    def load_reason_codes(self):
        for record in self.reason_codes:
            reason_code = ServiceReasonCodes(code=record['code'], description=record['description'])
            reason_code.save()

    def load_cart_types(self):
        for record in self.cart_types:
            cart_type = CartType(name=record['name'], size=record['size'])
            cart_type.save()

    def load_cart_status(self):
        for record in self.cart_status:
            cart_status = CartStatus(level=record['level'], label=record['label'])
            cart_status.save()

    def load_service_types(self):
        for record in self.service_types:
            service_type = CartServiceType(service=record['service'],
                                           code=record['code'], description=record['description'],
                                           complete_cart_status_change=
                                           CartStatus.objects.get(label=record['complete_cart_status_change'])
                                           )
            service_type.save()

    def load_ticket_status(self):
        for record in self.ticket_status:
            ticket_status = TicketStatus(level=record['level'],
                                         service_status=record['service_status'])
            ticket_status.save()