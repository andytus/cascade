from django.test import TestCase
from models import Cart, CollectionAddress, Owner
from django.utils import timezone



class ProcessCartUpload(TestCase):


    def test_create_a_upload_file(self):
        pass

    def test_process_cart_data(self):
        pass




class CartModelTest(TestCase):

    def test_creating_a_new_Cart_and_saving_it(self):
        """
        Test save of on Cart
        """
        cart = Cart()
        location = CollectionAddress()
        location.save()
        cart.owner =owner
        cart.rfid = "12345678910"
        cart.born_date = timezone.now()
        cart.cart_type = "Recycle"
        cart.location = location
        cart.current_status = "delivered"
        cart.serial_number = "1234"
        cart.last_updated = timezone.now()
        cart.size = 35
        cart.save()

        all_carts_in_database = Cart.objects.all()
        self.assertEqual(len(all_carts_in_database), 1)



