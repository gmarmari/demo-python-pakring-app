import unittest
from datetime import datetime
from rentals import Rental, RentalService


class TestRentals(unittest.TestCase):


    def test_rental(self):
        # Given
        licence_plate = "ABC 123"
        name = "Mickey"
        place_id = "1"
        rent_start = datetime(2024, 12, 1, 0, 0, 0)
        rent_end = datetime(2025, 12, 1, 0, 0, 0)

        # When
        rental = Rental(place_id, licence_plate, name, rent_start, rent_end)

        # Then
        self.assertEqual(rental.licence_plate, licence_plate)
        self.assertEqual(rental.name, name)
        self.assertEqual(rental.place_id, place_id)
        self.assertEqual(rental.rent_start, rent_start)
        self.assertEqual(rental.rent_end, rent_end)

    def test_rental_is_active_on_date(self):
        # Given
        licence_plate = "ABC 123"
        name = "Mickey"
        place_id = "1"
        rent_start = datetime(2024, 1, 1, 0, 0, 0)
        rent_end = datetime(2025, 1, 1, 0, 0, 0)
        rental = Rental(place_id, licence_plate, name, rent_start, rent_end)

        # When Then
        self.assertFalse(rental.is_active_on_date(datetime(2023, 12, 31, 23, 59, 59)))
        self.assertTrue(rental.is_active_on_date(datetime(2024, 1, 1, 0, 0, 0)))
        self.assertTrue(rental.is_active_on_date(datetime(2024, 1, 1, 0, 0, 1)))
        self.assertTrue(rental.is_active_on_date(datetime(2024, 12, 31, 23, 59, 59)))
        self.assertTrue(rental.is_active_on_date(datetime(2025, 1, 1, 0, 0, 0)))
        self.assertFalse(rental.is_active_on_date(datetime(2025, 1, 1, 0, 0, 1)))

    def test_rental_get_payment_amount_on_date(self): 
        # Given
        licence_plate = "ABC 123"
        name = "Mickey"
        place_id = "1"
        rent_start = datetime(2024, 1, 1, 0, 0, 0)
        rent_end = datetime(2025, 1, 1, 0, 0, 0)
        rental = Rental(place_id, licence_plate, name, rent_start, rent_end)

        # When Then
        self.assertEqual(rental.get_payment_amount_on_date(datetime(2023, 1, 1, 0, 0, 0)), 0)
        self.assertEqual(rental.get_payment_amount_on_date(datetime(2024, 1, 1, 0, 0, 0)), 0)
        self.assertEqual(rental.get_payment_amount_on_date(datetime(2024, 2, 1, 0, 0, 0)), 50)
        self.assertEqual(rental.get_payment_amount_on_date(datetime(2024, 7, 1, 0, 0, 0)), 300)
        self.assertEqual(rental.get_payment_amount_on_date(datetime(2025, 1, 1, 0, 0, 0)), 600)
        self.assertEqual(rental.get_payment_amount_on_date(datetime(2025, 6, 1, 0, 0, 0)), 600)


    def test_csv_delete_save_get(self):
        # Given 
        csv_service = RentalService()
        csv_service.csv_file = "csv/rentals_test.csv"
        rentalA = Rental("1", "ABC 1234", "Mickey", datetime(2024, 12, 1, 0, 0, 0), datetime(2025, 12, 1, 0, 0, 0))
        rentalB = Rental("6", "DEF 1234", "", datetime(2024, 12, 24, 8, 32, 47), datetime(2025, 12, 1, 0, 0, 0))

        # When
        self.assertTrue(csv_service.delete_rentals())
        self.assertTrue(csv_service.save_rental(rentalA))
        self.assertTrue(csv_service.save_rental(rentalB))
        list = csv_service.get_rentals()

        # Then
        self.assertEqual(len(list), 2)

        resultA : Rental = list[0]
        self.assertEqual(resultA.licence_plate, rentalA.licence_plate)
        self.assertEqual(resultA.name, rentalA.name)
        self.assertEqual(resultA.place_id, rentalA.place_id)
        self.assertEqual(resultA.rent_start, rentalA.rent_start)
        self.assertEqual(resultA.rent_end, rentalA.rent_end)

        resultB : Rental = list[1]
        self.assertEqual(resultB.licence_plate, rentalB.licence_plate)
        self.assertEqual(resultB.name, rentalB.name)
        self.assertEqual(resultB.place_id, rentalB.place_id)
        self.assertEqual(resultB.rent_start, rentalB.rent_start)
        self.assertEqual(resultB.rent_end, rentalB.rent_end)

    def test_get_active_rental_for_licence_plate(self):
        # Given 
        csv_service = RentalService()
        csv_service.csv_file = "csv/rentals_test.csv"
        rentalA = Rental("1", "ABC 1234", "Mickey", datetime(2024, 12, 1, 0, 0, 0), datetime(2025, 12, 1, 0, 0, 0))
        rentalB = Rental("2", "ABC 4321", "Mickey", datetime(2024, 1, 1, 0, 0, 0), datetime(2024, 2, 1, 0, 0, 0))

        # When
        self.assertTrue(csv_service.delete_rentals())
        self.assertTrue(csv_service.save_rental(rentalA))
        self.assertTrue(csv_service.save_rental(rentalB))

        resultA = csv_service.get_active_rental_for_licence_plate("ABC 1234")
        resultB = csv_service.get_active_rental_for_licence_plate("ABC 4321")
        resultC = csv_service.get_active_rental_for_licence_plate("not-found")

        # Then
        self.assertEqual(resultA.licence_plate, rentalA.licence_plate)
        self.assertEqual(resultA.name, rentalA.name)
        self.assertEqual(resultA.place_id, rentalA.place_id)
        self.assertEqual(resultA.rent_start, rentalA.rent_start)
        self.assertEqual(resultA.rent_end, rentalA.rent_end)

        self.assertIsNone(resultB)
        self.assertIsNone(resultC)


    def test_get_active_rental_for_place_id(self):
        # Given 
        csv_service = RentalService()
        csv_service.csv_file = "csv/rentals_test.csv"
        rentalA = Rental("1", "ABC 1234", "Mickey", datetime(2024, 12, 1, 0, 0, 0), datetime(2025, 12, 1, 0, 0, 0))
        rentalB = Rental("2", "ABC 4321", "Mickey", datetime(2024, 1, 1, 0, 0, 0), datetime(2024, 2, 1, 0, 0, 0))

        # When
        self.assertTrue(csv_service.delete_rentals())
        self.assertTrue(csv_service.save_rental(rentalA))
        self.assertTrue(csv_service.save_rental(rentalB))

        resultA = csv_service.get_active_rental_for_place_id("1")
        resultB = csv_service.get_active_rental_for_place_id("2")
        resultC = csv_service.get_active_rental_for_place_id("not-found")

        # Then
        self.assertEqual(resultA.licence_plate, rentalA.licence_plate)
        self.assertEqual(resultA.name, rentalA.name)
        self.assertEqual(resultA.place_id, rentalA.place_id)
        self.assertEqual(resultA.rent_start, rentalA.rent_start)
        self.assertEqual(resultA.rent_end, rentalA.rent_end)

        self.assertIsNone(resultB)
        self.assertIsNone(resultC)

    def test_get_active_rentals_on_date(self):
        # Given 
        csv_service = RentalService()
        csv_service.csv_file = "csv/rentals_test.csv"
        rentalA = Rental("1", "ABC 1234", "Mickey", datetime(2024, 1, 1, 0, 0, 0), datetime(2024, 6, 1, 0, 0, 0))
        rentalB = Rental("2", "ABC 4321", "Mickey", datetime(2024, 7, 1, 0, 0, 0), datetime(2025, 1, 1, 0, 0, 0))

        # When
        self.assertTrue(csv_service.delete_rentals())
        self.assertTrue(csv_service.save_rental(rentalA))
        self.assertTrue(csv_service.save_rental(rentalB))
        resultA = csv_service.get_active_rentals_on_date(datetime(2024, 3, 1, 0, 0, 0))
        resultB = csv_service.get_active_rentals_on_date(datetime(2024, 9, 1, 0, 0, 0))
        resultC = csv_service.get_active_rentals_on_date(datetime(2025, 3, 1, 0, 0, 0))

        # Then
        self.assertTrue(len(resultA) == 1)
        self.assertEqual(resultA[0].licence_plate, rentalA.licence_plate)
        self.assertTrue(len(resultB) == 1)
        self.assertEqual(resultB[0].licence_plate, rentalB.licence_plate)
        self.assertTrue(len(resultC) == 0)



if __name__ == '__main__':
    unittest.main()