import unittest
from datetime import datetime
from activities import Activity, ActivityService

class TestActivities(unittest.TestCase):

    def test_activity(self):
        # Given
        place_id = "1"
        licence_plate = "ABC 123"
        datetime_in = datetime(2024, 12, 1, 8, 0, 0)
        datetime_out = datetime(2024, 12, 9, 0, 0, 0)

        # When
        activity = Activity(place_id, licence_plate, datetime_in, datetime_out)

        # Then
        self.assertEqual(activity.place_id, place_id)
        self.assertEqual(activity.licence_plate, licence_plate)
        self.assertEqual(activity.datetime_in, datetime_in)
        self.assertEqual(activity.datetime_out, datetime_out)

    def test_activity_is_active(self):
        # Given
        place_id = "1"
        licence_plate = "ABC 123"
        activityA = Activity(place_id, licence_plate, datetime(2024, 12, 1, 8, 0, 0), datetime(2024, 12, 9, 0, 0, 0))
        activityB = Activity(place_id, licence_plate)

        # When # Then
        self.assertFalse(activityA.is_active())
        self.assertTrue(activityB.is_active())

    def test_csv_delete_save_get(self):
        # Given 
        csv_service = ActivityService()
        csv_service.csv_file = "csv/activity_test.csv"
        activityA = Activity("1", "ABC 1234", datetime(2024, 12, 1, 0, 0, 0))
        activityB = Activity("6", "DEF 1234", datetime(2024, 12, 24, 8, 32, 47), datetime(2024, 12, 24, 9, 32, 47))

        # When
        self.assertTrue(csv_service.delete_activities())
        self.assertTrue(csv_service.save_activity(activityA))
        self.assertTrue(csv_service.save_activity(activityB))
        list = csv_service.get_activities()

        # Then
        self.assertEqual(len(list), 2)

        resultA : Activity = list[0]
        self.assertEqual(resultA.place_id, activityA.place_id)
        self.assertEqual(resultA.licence_plate, activityA.licence_plate)
        self.assertEqual(resultA.datetime_in, activityA.datetime_in)
        self.assertEqual(resultA.datetime_out, activityA.datetime_out)

        resultB : Activity = list[1]
        self.assertEqual(resultB.place_id, activityB.place_id)
        self.assertEqual(resultB.licence_plate, activityB.licence_plate)
        self.assertEqual(resultB.datetime_in, activityB.datetime_in)
        self.assertEqual(resultB.datetime_out, activityB.datetime_out)

    def test_get_active_activity_for_licence_plate(self): 
         # Given 
        csv_service = ActivityService()
        csv_service.csv_file = "csv/activity_test.csv"
        activityA = Activity("1", "ABC 1234", datetime(2024, 12, 1, 0, 0, 0))
        activityB = Activity("6", "DEF 1234", datetime(2024, 12, 24, 8, 32, 47), datetime(2024, 12, 24, 9, 32, 47))
        self.assertTrue(csv_service.delete_activities())
        self.assertTrue(csv_service.save_activity(activityA))
        self.assertTrue(csv_service.save_activity(activityB))

        # When
        resultA = csv_service.get_active_activity_for_licence_plate("ABC 1234")
        resultB = csv_service.get_active_activity_for_licence_plate("DEF 1234")

        # Then
        self.assertEqual(resultA.place_id, activityA.place_id)
        self.assertEqual(resultA.licence_plate, activityA.licence_plate)
        self.assertEqual(resultA.datetime_in, activityA.datetime_in)
        self.assertEqual(resultA.datetime_out, activityA.datetime_out)

        self.assertIsNone(resultB)

    def test_get_active_activities(self) : 
         # Given 
        csv_service = ActivityService()
        csv_service.csv_file = "csv/activity_test.csv"
        activityA = Activity("1", "ABC 1234", datetime(2024, 12, 1, 0, 0, 0))
        activityB = Activity("6", "DEF 1234", datetime(2024, 12, 24, 8, 32, 47), datetime(2024, 12, 24, 9, 32, 47))
        self.assertTrue(csv_service.delete_activities())
        self.assertTrue(csv_service.save_activity(activityA))
        self.assertTrue(csv_service.save_activity(activityB))

        # When
        list = csv_service.get_active_activities()

        # Then
        self.assertEqual(len(list), 1)

        resultA = list[0]
        self.assertEqual(resultA.place_id, activityA.place_id)
        self.assertEqual(resultA.licence_plate, activityA.licence_plate)
        self.assertEqual(resultA.datetime_in, activityA.datetime_in)
        self.assertEqual(resultA.datetime_out, activityA.datetime_out)

    def test_get_active_activity_for_place_id(self): 
         # Given 
        csv_service = ActivityService()
        csv_service.csv_file = "csv/activity_test.csv"
        activityA = Activity("1", "ABC 1234", datetime(2024, 12, 1, 0, 0, 0))
        activityB = Activity("6", "DEF 1234", datetime(2024, 12, 24, 8, 32, 47), datetime(2024, 12, 24, 9, 32, 47))
        self.assertTrue(csv_service.delete_activities())
        self.assertTrue(csv_service.save_activity(activityA))
        self.assertTrue(csv_service.save_activity(activityB))

        # When
        resultA = csv_service.get_active_activity_for_place_id("1")
        resultB = csv_service.get_active_activity_for_place_id("6")

        # Then
        self.assertEqual(resultA.place_id, activityA.place_id)
        self.assertEqual(resultA.licence_plate, activityA.licence_plate)
        self.assertEqual(resultA.datetime_in, activityA.datetime_in)
        self.assertEqual(resultA.datetime_out, activityA.datetime_out)

        self.assertIsNone(resultB)
    

    def test_update_activity(self): 
         # Given 
        csv_service = ActivityService()
        csv_service.csv_file = "csv/activity_test.csv"
        activityA = Activity("1", "ABC 1234", datetime(2024, 12, 1, 0, 0, 0))
        self.assertTrue(csv_service.delete_activities())
        self.assertTrue(csv_service.save_activity(activityA))

        # When
        resultBefore = csv_service.get_active_activity_for_licence_plate("ABC 1234")
        csv_service.update_activity("ABC 1234", datetime(2024, 12, 1, 10, 0, 0))
        resultAfter = csv_service.get_active_activity_for_licence_plate("ABC 1234")

        # Then
        self.assertIsNotNone(resultBefore)
        self.assertIsNone(resultAfter)



if __name__ == '__main__':
    unittest.main()