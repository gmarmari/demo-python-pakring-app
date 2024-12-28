import unittest
from unittest.mock import Mock
from datetime import datetime
from controller import ParkingController 
from activities import Activity
from rentals import Rental
from parking_spaces import ParkingSpace

class TestControllerCreateRental(unittest.TestCase):

    def test_get_free_long_term_parking_spaces_for_dates(self):
        # Given 
        license_plate = "ABC 1234"
        view = Mock()
        parking_space_service = Mock()
        rental_service = Mock()

        parking_space_service.get_long_term_parking_spaces.return_value = [ParkingSpace("1", True), ParkingSpace("2", True), ParkingSpace("3", True)]
        rental_service.get_active_rentals_on_date.return_value = [Rental("1", "DEF123")]

        p = ParkingController(parking_space_service=parking_space_service, rental_service=rental_service)
        p.view = view

        # When
        list = p.get_free_long_term_parking_spaces_for_dates()

        # Then
        self.assertEquals(list, ["2", "3"])

    def test_handle_create_rental_with_invalid_dates(self) :
                # Given 
        license_plate = "ABC 1234"
        name = "Mickey"
        place_id = "3"
        date_start = "01-02-2025"
        date_end = "01-01-2025"
        view = Mock()
        parking_space_service = Mock()
        rental_service = Mock()

        parking_space_service.get_long_term_parking_spaces.return_value = [ParkingSpace("1", True), ParkingSpace("2", True), ParkingSpace("3", True)]
        rental_service.get_active_rentals_on_date.return_value = [Rental("1", "DEF123")]

        p = ParkingController(parking_space_service=parking_space_service, rental_service=rental_service)
        p.view = view

        # When
        list = p.handle_create_rental(license_plate, name, place_id, date_start, date_end)

        # Then
        view.error_invalid_start_end_date.assert_called

    def test_handle_create_rental_when_active_rental_for_place_exists(self) :
        # Given 
        license_plate = "ABC 1234"
        name = "Mickey"
        place_id = "3"
        date_start = "01-01-2025"
        date_end = "01-01-2026"
        view = Mock()
        parking_space_service = Mock()
        rental_service = Mock()

        parking_space_service.get_long_term_parking_spaces.return_value = [ParkingSpace("1", True), ParkingSpace("2", True), ParkingSpace("3", True)]
        rental_service.get_active_rentals_on_date.return_value = [Rental("1", "DEF123")]

        rental_service.get_active_rental_for_place_id.return_value = [Rental("3", "DEF123")]

        p = ParkingController(parking_space_service=parking_space_service, rental_service=rental_service)
        p.view = view

        # When
        list = p.handle_create_rental(license_plate, name, place_id, date_start, date_end)

        # Then
        view.error_place_is_not_available_for_rental.assert_called_with("3")

    def test_handle_create_rental_when_success(self) :
        # Given 
        license_plate = "ABC 1234"
        name = "Mickey"
        place_id = "3"
        date_start = "01-01-2025"
        date_end = "01-01-2026"
        view = Mock()
        parking_space_service = Mock()
        rental_service = Mock()

        parking_space_service.get_long_term_parking_spaces.return_value = [ParkingSpace("1", True), ParkingSpace("2", True), ParkingSpace("3", True)]
        rental_service.get_active_rentals_on_date.return_value = [Rental("1", "DEF123")]


        p = ParkingController(parking_space_service=parking_space_service, rental_service=rental_service)
        p.view = view

        # When
        list = p.handle_create_rental(license_plate, name, place_id, date_start, date_end)

        # Then
        rental_service.save_rental.assert_called
        view.show_rental_saved.assert_called 

    

   


if __name__ == '__main__':
    unittest.main()