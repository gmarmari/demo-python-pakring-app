import unittest
from unittest.mock import Mock
from datetime import datetime
from controller import ParkingController 
from activities import Activity
from rentals import Rental
from short_term_rental_payments import ShortTermRentalPayment

class TestControllerDaysTakings(unittest.TestCase):


    def test_get_payments_for_today(self):
        # Given 
        license_plate = "ABC 1234"
        view = Mock()
        payment_service = Mock()

        paymentA  = ShortTermRentalPayment("1", "ABC 1234", 4, datetime(2024, 1, 1, 8, 0, 0))
        paymentB  = ShortTermRentalPayment("2", "DEF 1234", 2, datetime(2024, 1, 2, 9, 0, 0))
        payment_service.get_payments_for_today.return_value = [paymentA, paymentB]

        p = ParkingController(payment_service=payment_service)
        p.view = view

        # When
        list = p.get_payments_for_today()

        # Then
        self.assertTrue(len(list) == 2)


    def test_get_total_amount_of_payments_for_today(self):
        # Given 
        license_plate = "ABC 1234"
        view = Mock()
        payment_service = Mock()

        paymentA  = ShortTermRentalPayment("1", "ABC 1234", 4, datetime(2024, 1, 1, 8, 0, 0))
        paymentB  = ShortTermRentalPayment("2", "DEF 1234", 6, datetime(2024, 1, 2, 9, 0, 0))
        paymentC  = ShortTermRentalPayment("2", "HJK 1234", 8, datetime(2024, 1, 2, 10, 0, 0))
        payment_service.get_payments_for_today.return_value = [paymentA, paymentB, paymentC]

        p = ParkingController(payment_service=payment_service)
        p.view = view

        # When
        amount = p.get_total_amount_of_payments_for_today()

        # Then
        self.assertEqual(amount, 18)



if __name__ == '__main__':
    unittest.main()