import unittest
from unittest.mock import Mock
from datetime import datetime
from controller import ParkingController 
from parking_spaces import ParkingSpace, ParkingSpaceOverview
from activities import Activity

class TestControllerParkedCars(unittest.TestCase):


    def test_get_active_activities(self):
        # Given 
        view = Mock()
        activity_service = Mock()

        p = ParkingController(activity_service=activity_service)
        p.view = view

        # When
        list = p.get_active_activities()

        # Then
        activity_service.get_active_activities.assert_called



if __name__ == '__main__':
    unittest.main()