import unittest
from datetime import datetime
from short_term_rental_payments import ShortTermRentalPayment, ShortTermRentalPaymentService

class TestShortTermRentalPayments(unittest.TestCase):


    def test_short_term_rental_payment(self):
        # Given
        place_id = "1"
        licence_plate = "ABC 123"
        amount = 6
        date = datetime(2024, 12, 1, 8, 0, 0)

        # When
        payment = ShortTermRentalPayment(place_id, licence_plate, amount, date)

        # Then
        self.assertEqual(payment.place_id, place_id)
        self.assertEqual(payment.licence_plate, licence_plate)
        self.assertEqual(payment.amount, amount)
        self.assertEqual(payment.date, date)

def test_csv_delete_save_get(self):
        # Given 
        csv_service = ShortTermRentalPaymentService()
        csv_service.csv_file = "csv/short_term_rental_payment_test.csv"
        paymentA = ShortTermRentalPayment("1", "ABC 1234", 4, datetime(2024, 12, 1, 0, 0, 0))
        paymentB = ShortTermRentalPayment("6", "DEF 1234", 6, datetime(2024, 12, 24, 8, 32, 47))

        # When
        self.assertTrue(csv_service.delete_payments())
        self.assertTrue(csv_service.save_payment(paymentA))
        self.assertTrue(csv_service.save_payment(paymentB))
        list = csv_service.get_payments()

        # Then
        self.assertEqual(len(list), 2)

        resultA : ShortTermRentalPayment = list[0]
        self.assertEqual(resultA.place_id, paymentA.place_id)
        self.assertEqual(resultA.licence_plate, paymentA.licence_plate)
        self.assertEqual(resultA.amount, paymentA.amount)
        self.assertEqual(resultA.date, paymentA.date)

        resultB : ShortTermRentalPayment = list[1]
        self.assertEqual(resultB.place_id, paymentB.place_id)
        self.assertEqual(resultB.licence_plate, paymentB.licence_plate)
        self.assertEqual(resultB.amount, paymentB.amount)
        self.assertEqual(resultB.date, paymentB.date)



if __name__ == '__main__':
    unittest.main()