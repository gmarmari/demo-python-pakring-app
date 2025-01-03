import unittest
from unittest.mock import Mock
from datetime import datetime
from controller import ParkingController 
from short_term_rental_payments import ShortTermRentalPayment
from rentals import Rental

class TestControllerTotalTakings(unittest.TestCase):


    def test_get_total_takings(self):
        # Given 
        license_plate = "ABC 1234"
        view = Mock()
        payment_service = Mock()
        rental_service = Mock()

        paymentA  = ShortTermRentalPayment("1", "ABC 1234", 4, datetime(2024, 1, 1, 8, 0, 0))
        paymentB  = ShortTermRentalPayment("2", "DEF 1234", 6, datetime(2024, 1, 2, 9, 0, 0))
        payment_service.get_payments.return_value = [paymentA, paymentB]

        rental = Rental("3", "GEF 1234", "Mickey", datetime(2024, 1, 1, 0, 0, 0), datetime(2025, 1, 1, 0, 0, 0))
        rental_service.get_rentals.return_value = [rental]

        p = ParkingController(payment_service=payment_service, rental_service=rental_service)
        p.view = view

        # When
        list = p.get_total_takings()

        # Then
        self.assertTrue(len(list) ==3)
        self.assertEqual(list[0].licence_plate, "GEF 1234")
        self.assertEqual(list[0].amount, 600)
        self.assertEqual(list[1].licence_plate, "DEF 1234")
        self.assertEqual(list[1].amount, 6)
        self.assertEqual(list[2].licence_plate, "ABC 1234")
        self.assertEqual(list[2].amount, 4)


if __name__ == '__main__':
    unittest.main()