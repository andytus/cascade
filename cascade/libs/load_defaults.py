__author__ = 'jbennett'

from django.contrib.sites.models import Site
from cascade.apps.cartmanager.models import CartStatus, CartType, TicketStatus, CartServiceType


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

    def load_cart_types(self):
        for record in self.cart_types:
            cart_type = CartType(site=Site.objects.get(pk=self.default_site), name=record['name'], size=record['size'])
            cart_type.save()

    def load_cart_status(self):
        for record in self.cart_status:
            cart_status = CartStatus(site=Site.objects.get(pk=self.default_site), level=record['level'], label=record['label'])
            cart_status.save()

    def load_service_types(self):
        for record in self.service_types:
            service_type = CartServiceType(site=Site.objects.get(pk=self.default_site), service=record['service'],
                                           code=record['code'], description=record['description'],
                                           complete_cart_status_change=
                                           CartStatus.objects.get(label=record['complete_cart_status_change'])
                                           )
            service_type.save()

    def load_ticket_status(self):
        for record in self.ticket_status:
            ticket_status = TicketStatus(site=self.default_site, level=record['level'],
                                         service_status=record['service_status'])
            ticket_status.save()