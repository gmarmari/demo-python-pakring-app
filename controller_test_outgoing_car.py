import unittest
from unittest.mock import Mock
from datetime import datetime
from controller import ParkingController 
from activities import Activity
from rentals import Rental

class TestControllerOutgoingCar(unittest.TestCase):


    def test_handle_outgoing_car_when_active_rental_exists_then_show_goodbye(self):
        # Given 
        license_plate = "ABC 1234"
        view = Mock()
        rental_service = Mock()

        rent_start = datetime(2024, 1, 1, 0, 0, 0)
        rent_end = datetime(2050, 1, 1, 0, 0, 0)
        rental_service.get_active_rental_for_licence_plate.return_value = Rental("1", license_plate, "Max", rent_start, rent_end)

        p = ParkingController(rental_service=rental_service)
        p.view = view

        # When
        p.handle_outgoing_car(license_plate)

        # Then
        view.show_goodbye_message.assert_called_with("ABC 1234")

    def test_handle_outgoing_car_when_no_active_activity_then_show_error(self):
        # Given 
        license_plate = "ABC 1234"
        view = Mock()
        rental_service = Mock()
        activity_service = Mock()

        rental_service.get_active_rental_for_licence_plate.return_value = None

        activity_service.get_active_activity_for_licence_plate.return_value = None

        p = ParkingController(rental_service=rental_service, activity_service=activity_service)
        p.view = view

        # When
        p.handle_outgoing_car(license_plate)

        # Then
        view.error_no_incoming_activity_found.assert_called_with("ABC 1234")


    def test_handle_outgoing_car_when_active_activity_then_show_info(self):
        # Given 
        license_plate = "ABC 1234"
        view = Mock()
        rental_service = Mock()
        parking_space_service = Mock()
        activity_service = Mock()
        payment_service = Mock()

        rental_service.get_active_rental_for_licence_plate.return_value = None

        activity_service.get_active_activity_for_licence_plate.return_value = Activity("1", license_plate)

        p = ParkingController(rental_service, parking_space_service, activity_service, payment_service)
        p.view = view

        # When
        p.handle_outgoing_car(license_plate)

        # Then
        activity_service.update_activity.assert_called
        parking_space_service.update_parking_space.assert_called
        payment_service.save_payment.assert_called

        view.show_goodbye_with_payment_message.assert_called_with("ABC 1234", 2)



if __name__ == '__main__':
    unittest.main()