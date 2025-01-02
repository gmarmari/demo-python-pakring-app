import unittest
from datetime import datetime
from date_utils import DateUtils

class TestDateUtils(unittest.TestCase):

    def test_months_difference(self):
        # Given
        date1 = datetime(2023, 5, 15, 0, 0, 0)
        date2 = datetime(2025, 1, 1, 0, 0, 0)
        date3 = datetime(2025, 5, 15, 0, 0, 0)
        date4 = datetime(2025, 6, 1, 0, 0, 0)

        # When
        resultA = DateUtils().months_difference(date1, date2)
        resultB = DateUtils().months_difference(date2, date3)
        resultC = DateUtils().months_difference(date1, date3)
        resultD = DateUtils().months_difference(date3, date4)

        # Then
        self.assertEqual(resultA, 20)
        self.assertEqual(resultB, 4)
        self.assertEqual(resultC, 24)
        self.assertEqual(resultD, 1)

    
    
if __name__ == '__main__':
    unittest.main()