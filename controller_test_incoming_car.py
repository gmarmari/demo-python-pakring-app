import unittest
from unittest.mock import Mock
from datetime import datetime
from controller import ParkingController 
from activities import Activity
from rentals import Rental
from parking_spaces import ParkingSpace

class TestControllerIncomingCar(unittest.TestCase):



    def test_handle_incoming_car_when_active_activity_exists_then_show_info(self):
        # Given 
        license_plate = "ABC 1234"
        view = Mock()
        activity_service = Mock()

        rent_start = datetime(2024, 1, 1, 0, 0, 0)
        rent_end = datetime(2050, 1, 1, 0, 0, 0)
        activity_service.get_active_activity_for_licence_plate.return_value = Activity("1", license_plate)

        p = ParkingController(activity_service=activity_service)
        p.view = view

        # When
        p.handle_incoming_car(license_plate)

        # Then
        view.show_parking_place.assert_called_with("ABC 1234", "1")

    def test_handle_incoming_car_when_long_term_rental_exists_then_show_info(self):
        # Given 
        license_plate = "ABC 1234"
        view = Mock()
        rental_service = Mock()

        rent_start = datetime(2024, 1, 1, 0, 0, 0)
        rent_end = datetime(2050, 1, 1, 0, 0, 0)
        rental_service.get_active_rental_for_licence_plate.return_value = Rental("1", license_plate, "", rent_start, rent_end)

        p = ParkingController(rental_service)
        p.view = view

        # When
        p.handle_incoming_car(license_plate)

        # Then
        view.show_parking_place.assert_called_with("ABC 1234", "1")

    def test_handle_incoming_car_when_no_rental_exists_then_find_the_next_available_space(self):
        # Given 
        license_plate = "CBA 9876"
        view = Mock()
        rental_service = Mock()
        parking_space_service = Mock()

        rental_service.get_active_rental_for_licence_plate.return_value = None
        parking_space_service.get_next_free_short_term_space.return_value = ParkingSpace("7", False, True)

        p = ParkingController(rental_service, parking_space_service)
        p.view = view

        # When
        p.handle_incoming_car(license_plate)

        # Then
        view.show_parking_place.assert_called_with("CBA 9876", "7")

    def test_handle_incoming_car_when_no_rental_exists_and_parking_full_then_show_error(self):
        # Given 
        license_plate = "CBA 9876"
        view = Mock()
        rental_service = Mock()
        parking_space_service = Mock()
        activity_service = Mock()

        activity_service.get_active_activity_for_licence_plate.return_value = None
        rental_service.get_active_rental_for_licence_plate.return_value = None
        parking_space_service.get_next_free_short_term_space.return_value = None

        p = ParkingController(rental_service, parking_space_service, activity_service)
        p.view = view

        # When
        p.handle_incoming_car(license_plate)

        # Then
        view.error_no_short_term_place_available.assert_called()


if __name__ == '__main__':
    unittest.main()