import unittest
from datetime import datetime
from parking_spaces import ParkingSpace, ParkingSpaceService

class TestParkingSpaces(unittest.TestCase):


    def test_parking_space(self):
        # Given
        id = "1"
        licence_plate = "ABC 123"

        # When
        space = ParkingSpace(id)

        # Then
        self.assertEqual(space.place_id, id)
        self.assertTrue(space.is_free)
       

    def test_csv_save_get_update(self):
        # Given 
        csv_service = ParkingSpaceService()
        csv_service.csv_file = "csv/parking_spaces_test.csv"
        spaceA = ParkingSpace("1", True, True)
        spaceB = ParkingSpace("2", False, True)

        # When
        self.assertTrue(csv_service.save_parking_spaces([spaceA, spaceB]))
        csv_service.update_parking_space("2", False)
        list = csv_service.get_parking_spaces()

        # Then
        self.assertEqual(len(list), 2)

        resultA : ParkingSpace = list[0]
        self.assertEqual(resultA.place_id, spaceA.place_id)
        self.assertEqual(resultA.long_term, spaceA.long_term)
        self.assertEqual(resultA.is_free, spaceA.is_free)

        resultB : ParkingSpace = list[1]
        self.assertEqual(resultB.place_id, spaceB.place_id)
        self.assertEqual(resultB.long_term, spaceB.long_term)
        self.assertEqual(resultB.is_free, False)

    def test_get_next_free_short_term_space(self):
        # Given 
        csv_service = ParkingSpaceService()
        csv_service.csv_file = "csv/parking_spaces_test.csv"
        spaceA = ParkingSpace("1", True, False)
        spaceB = ParkingSpace("2", False, True)

        # When
        self.assertTrue(csv_service.save_parking_spaces([spaceA, spaceB]))
        result = csv_service.get_next_free_short_term_space()

        # Then
        self.assertEqual(result.place_id, spaceB.place_id)
        self.assertEqual(result.long_term, spaceB.long_term)
        self.assertEqual(result.is_free, spaceB.is_free)


if __name__ == '__main__':
    unittest.main()