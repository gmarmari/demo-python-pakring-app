from datetime import datetime
import os
import csv
import logging
from csv_service import BaseCsvService


class Activity:
  def __init__(self, place_id: str, licence_plate : str, datetime_in : datetime = datetime.now(), datetime_out : datetime = None):
    self.licence_plate = licence_plate
    self.place_id = place_id
    self.datetime_in = datetime_in
    self.datetime_out = datetime_out

  def is_active(self) -> bool:
    return self.datetime_out is None

class ActivityService(BaseCsvService):
    def __init__(self, csv_file : str = 'csv/activity.csv'):
        super().__init__(csv_file)
        self._activities : list = None
    
    def get_activities(self) -> list:
        if self._activities is not None :
            return self._activities

        self._activities = []
        try:
            with open(self.csv_file , mode='r', newline='',encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    place_id = row[0]
                    licence_plate =  row[1]
                    datetime_in = self._str_to_datetime(row[2])
                    datetime_out = self._str_to_datetime(row[3])
                    self._activities.append(Activity(place_id, licence_plate, datetime_in, datetime_out))
        except Exception:
            logging.exception("Error reading activities from csv file")
            pass
        return self._activities
    
    def get_active_activity_for_licence_plate(self, licence_plate: str) -> Activity:
        try:
            return next(a for a in self.get_activities() if a.licence_plate == licence_plate and a.is_active() == True)
        except Exception:
            return None  
        
    def get_active_activity_for_place_id(self, place_id: str) -> Activity:
        try:
            return next(a for a in self.get_activities() if a.place_id == place_id and a.is_active() == True)
        except Exception:
            return None  
    
    def save_activity(self, a: Activity) -> bool:
        try:
            with open(self.csv_file ,'a',newline='',encoding='utf-8') as f:
                writer = csv.writer(f)
                if os.path.getsize(self.csv_file) == 0:
                    writer.writerow(['place_id','licence_plate','datetime_in','datetime_out'])
                writer.writerow([
                    a.place_id, 
                    a.licence_plate, 
                    self._datetime_to_str(a.datetime_in),
                    self._datetime_to_str(a.datetime_out) 
                    ])
                self._activities = None
            return True
        except Exception:
            logging.exception("Error saving activity to csv file")
            return False
        
    def save_activities(self, activities: list) -> bool:
        try:
            with open(self.csv_file ,'w',newline='',encoding='utf-8') as f:
                writer = csv.writer(f)
                if os.path.getsize(self.csv_file) == 0:
                    writer.writerow(['place_id','licence_plate','datetime_in','datetime_out'])
                for a in activities:
                    writer.writerow([
                    a.place_id, 
                    a.licence_plate, 
                    self._int_to_str(a.datetime_in),
                    self._datetime_to_str(a.datetime_out) 
                    ])
                self._activities = None
                return True
        except Exception:
            logging.exception("Error saving activities to csv file")
            return False
        
    def update_activity(self, licence_plate: str, datetime_out : datetime) -> bool: 
        activity = self.get_active_activity_for_licence_plate(licence_plate)
        if activity is None:
            return False
        activity.datetime_out = datetime_out
        self.save_activities(self._activities)
        return True



    def delete_activities(self) -> bool:
        try:
            self._delete_content()
            self._activities = None
            return True
        except Exception:
            logging.exception("Error deleting activities from csv file")
            return False