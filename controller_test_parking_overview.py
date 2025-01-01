import unittest
from unittest.mock import Mock
from datetime import datetime
from controller import ParkingController 
from parking_spaces import ParkingSpace, ParkingSpaceOverview
from activities import Activity

class TestControllerParkingSpaceOverview(unittest.TestCase):


    def test_handle_outgoing_car_when_active_rental_exists_then_show_goodbye(self):
        # Given 
        license_plate = "ABC 1234"
        view = Mock()
        parking_space_service = Mock()
        activity_service = Mock()

        parking_space_service.get_parking_spaces.return_value = [ParkingSpace("1", True, True), ParkingSpace("2", False, False)]
        activity_service.get_active_activity_for_place_id.return_value = Activity("2", "ABC 1234")

        p = ParkingController(parking_space_service=parking_space_service, activity_service=activity_service)
        p.view = view

        # When
        list = p.get_parking_spaces_overview()


        # Then
        self.assertEqual(len(list), 2)
        spaceA : ParkingSpaceOverview = list[0]
        self.assertEqual(spaceA.text, "1")
        self.assertEqual(spaceA.background, "yellow")
        self.assertEqual(spaceA.row, 0)
        self.assertEqual(spaceA.column, 0)

        spaceA : ParkingSpaceOverview = list[1]
        self.assertEqual(spaceA.text, "2 - ABC 1234")
        self.assertEqual(spaceA.background, "lightblue")
        self.assertEqual(spaceA.row, 0)
        self.assertEqual(spaceA.column, 1)



if __name__ == '__main__':
    unittest.main()