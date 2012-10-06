from django.test import TestCase
from models import Cart, CollectionAddress, Owner
from django.utils import timezone


class CartModelTest(TestCase):

    def test_creating_a_new_Cart_and_saving_it(self):
        cart = Cart()
        cart.owner = Owner()
        cart.rfid = "12345678910"
        cart.born_date = timezone.now()
        cart.cart_type = "Recycle"
        cart.location = CollectionAddress()
        cart.current_status = "delivered"
        cart.serial_number = "1234"
        cart.last_updated = timezone.now()
        cart.size = 35

