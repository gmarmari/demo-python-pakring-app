import os
import csv
import logging
from csv_service import BaseCsvService

class ParkingSpace:
  def __init__(self, place_id : str, long_term : bool = False, is_free: bool = True):
    self.place_id = place_id
    self.long_term = long_term
    self.is_free = is_free

class ParkingSpaceOverview:
  def __init__(self, text : str,  background : str = "lightblue", row : int = 0, column: int = 0):
    self.text = text
    self.background = background
    self.row = row
    self.column = column


class ParkingSpaceService(BaseCsvService):
    def __init__(self, csv_file : str = 'csv/parking_spaces.csv'):
        super().__init__(csv_file)
        self._parking_spaces : list = None
        self.get_parking_spaces() # fills self._parking_spaces
        if len(self._parking_spaces) == 0 : 
            self.save_parking_spaces([ParkingSpace("1", True), ParkingSpace("2", True), ParkingSpace("3", True), ParkingSpace("4", True), ParkingSpace("5", True),
                  ParkingSpace("6"), ParkingSpace("7"), ParkingSpace("8"),ParkingSpace("9"), ParkingSpace("10"),
                  ParkingSpace("11"), ParkingSpace("12"), ParkingSpace("13"),ParkingSpace("14"), ParkingSpace("15"),
                  ParkingSpace("16"), ParkingSpace("17"), ParkingSpace("18"),ParkingSpace("19"), ParkingSpace("20")])

    def get_parking_spaces(self) -> list:
        if self._parking_spaces is not None :
            return self._parking_spaces

        self._parking_spaces = []
        try:
            with open(self.csv_file , mode='r', newline='',encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    place_id = row[0]
                    long_term = self._str_to_bool(row[1])
                    is_free = self._str_to_bool(row[2])
                    self._parking_spaces.append(ParkingSpace(place_id, long_term, is_free))
        except Exception:
            logging.exception("Error reading parking spaces from csv file")
            pass
        return self._parking_spaces
    
    def get_long_term_parking_spaces(self) -> list:
        return list(filter(lambda p: p.long_term == True, self.get_parking_spaces()))
    
    def get_free_parking_spaces(self) -> list:
        return list(filter(lambda p: p.is_free == True, self.get_parking_spaces()))
    
    def get_next_free_short_term_space(self) -> ParkingSpace:
      try:
        return next(s for s in self.get_parking_spaces() if s.long_term == False and s.is_free == True)
      except Exception:
        return None  
    
    def update_parking_space(self, place_id: str, is_free: bool) : 
        if self._parking_spaces is None:
            self.get_parking_spaces()
        try:
            foundPlace = next(s for s in self._parking_spaces if s.place_id == place_id)
            foundPlace.is_free = is_free
            self.save_parking_spaces(self._parking_spaces)
            return True
        except Exception:
            logging.exception("Error saving parking spaces to csv file")
            return False


    def save_parking_spaces(self, parking_spaces: list) -> bool:
        try:
            with open(self.csv_file ,'w',newline='',encoding='utf-8') as f:
                writer = csv.writer(f)
                if os.path.getsize(self.csv_file) == 0:
                    writer.writerow(['place_id','long_term','is_free'])
                for s in parking_spaces:
                    writer.writerow([
                        s.place_id, 
                        self._bool_to_str(s.long_term),
                        self._bool_to_str(s.is_free),
                        ])
                self._parking_spaces = None
                return True
        except Exception:
            logging.exception("Error saving parking spaces to csv file")
            return False
        