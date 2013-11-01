from django.test import TestCase, TransactionTestCase
from django.test.client import Client
from cascade.apps.cartmanager.models import Cart, CollectionAddress
from django.utils import timezone



# class CartModelTest(TestCase):
#
#     def test_creating_a_new_Cart(self):
#         """
#         Test save of on Cart
#         """
#         cart = Cart()
#         location = CollectionAddress()
#         location.save()
#         cart.owner =owner
#         cart.rfid = "12345678910"
#         cart.born_date = timezone.now()
#         cart.cart_type = "Recycle"
#         cart.location = location
#         cart.current_status = "delivered"
#         cart.serial_number = "1234"
#         cart.last_updated = timezone.now()
#         cart.size = 35
#         cart.save()
#
#         all_carts_in_database = Cart.objects.all()
#         self.assertEqual(len(all_carts_in_database), 1)


class TestClient(Client):
    pass

class TemplateViewTest(TestCase):

    fixtures = ['initial.json']

    def setUp(self):
        self.client.login(username='jbennett', password='charlize20')

    def test_file_upload_list_view(self):
        response = self.client.get('/carts/upload/files', HTTP_HOST='127.0.0.1:8000', follow=True)
        self.assertEqual(response.status_code, 200, "Did not return 200")

    def test_cart_search_list_view(self):
        response = self.client.get('/carts/cart/search/', HTTP_HOST='127.0.0.1:8000', follow=True)
        self.assertEqual(response.status_code, 200, "Did not return 200")

    def test_cart_report_view(self):
        response = self.client.get('/carts/cart/report/', HTTP_HOST='127.0.0.1:8000', follow=True)
        self.assertEqual(response.status_code, 200, "Did not return 200")

    def test_cart_profile_view(self):
        response = self.client.get('/carts/cart/profile/1000000', HTTP_HOST='127.0.0.1:8000', follow=True)
        self.assertEqual(response.status_code, 200, "Did not return 200")

    def test_cart_new(self):
        response = self.client.get('/carts/cart/new/', HTTP_HOST='127.0.0.1:8000', follow=True)
        self.assertEqual(response.status_code, 200, "Did not return 200")

    def test_cart_address_change(self):
        response = self.client.get('/carts/cart/profile/update/location/1000000', HTTP_HOST='127.0.0.1:8000', follow=True)
        self.assertEqual(response.status_code, 200, "Did not return 200")

    def test_customer_profile(self):
        response = self.client.get('/carts/customer/profile/1000000', HTTP_HOST='127.0.0.1:8000', follow=True)
        self.assertEqual(response.status_code, 200, "Did not return 200")

    def test_customer_new(self):
        response = self.client.get('/carts/customer/new/', HTTP_HOST='127.0.0.1:8000', follow=True)
        self.assertEqual(response.status_code, 200, "Did not return 200")

    def test_customer_report(self):
        response = self.client.get('/carts/customer/report/', HTTP_HOST='127.0.0.1:8000', follow=True)
        self.assertEqual(response.status_code, 200, "Did not return 200")

    def test_location_search(self):
        response = self.client.get('/carts/location/search/', HTTP_HOST='127.0.0.1:8000', follow=True)
        self.assertEqual(response.status_code, 200, "Did not return 200")

    def test_upload_files(self):
        response = self.client.get('/carts/upload/files/', HTTP_HOST='127.0.0.1:8000', follow=True)
        self.assertEqual(response.status_code, 200, "Did not return 200")

    def test_tickets_report(self):
        response = self.client.get('/carts/tickets/report/', HTTP_HOST='127.0.0.1:8000', follow=True)
        self.assertEqual(response.status_code, 200, "Did not return 200")

    def test_ticket_new(self):
        response = self.client.get('/carts/ticket/new', HTTP_HOST='127.0.0.1:8000', follow=True)
        self.assertEqual(response.status_code, 200, "Did not return 200")

    def test_ticket_profile(self):
        response = self.client.get('/carts/ticket/profile/00000000', HTTP_HOST='127.0.0.1:8000', follow=True)
        self.assertEqual(response.status_code, 200, "Did not return 200")

    def test_route_upload(self):
        response = self.client.get('/carts/upload/routes/', HTTP_HOST='127.0.0.1:8000', follow=True)
        self.assertEqual(response.status_code, 200, "Did not return 200")

    def test_cart_upload(self):
        response = self.client.get('/carts/upload/carts/', HTTP_HOST='127.0.0.1:8000', follow=True)
        self.assertEqual(response.status_code, 200, "Did not return 200")

    def test_customer_upload(self):
        response = self.client.get('/carts/upload/customers/', HTTP_HOST='127.0.0.1:8000', follow=True)
        self.assertEqual(response.status_code, 200, "Did not return 200")

    def test_upload_errors(self):
        response = self.client.get('/carts/upload/errors/', HTTP_HOST='127.0.0.1:8000', follow=True)
        self.assertEqual(response.status_code, 200, "Did not return 200")

































