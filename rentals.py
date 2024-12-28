from datetime import datetime
import os
import csv
import logging
from csv_service import BaseCsvService

class Rental:
  def __init__(self, place_id: str, licence_plate : str, name : str = "", rent_start : datetime = datetime.now(), rent_end : datetime = datetime.now()):
    self.licence_plate = licence_plate
    self.name = name
    self.place_id = place_id
    self.rent_start = rent_start
    self.rent_end = rent_end

  def is_active(self) -> bool:
    return self.is_active_on_date(datetime.now())
  
  def is_active_on_date(self, date: datetime) -> bool :
      """
      return true if the gievn date is between the renta_start date and rent_end date
      """
      return date >= self.rent_start and date <= self.rent_end
      
      
  

class RentalService(BaseCsvService):
    def __init__(self, csv_file : str = 'csv/rentals.csv'):
        super().__init__(csv_file)
        self._rentals : list = None

    def get_rentals(self) -> list:
        if self._rentals is not None :
            return self._rentals
        self._rentals = []
        try:
            with open(self.csv_file , mode='r', newline='',encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    licence_plate = row[0]
                    name = row[1]
                    place_id = row[2]
                    rent_start = self._str_to_datetime(row[3])
                    rent_end = self._str_to_datetime(row[4])
                    self._rentals.append(Rental(place_id, licence_plate, name, rent_start, rent_end))
        except Exception:
            logging.exception("Error reading rentals from csv file")
            pass
        return self._rentals
    
    
    def get_active_rental_for_licence_plate(self, licence_plate : str) -> Rental: 
        try:
            return next(r for r in self.get_rentals() if r.licence_plate == licence_plate and r.is_active() == True)
        except Exception:
            return None  
        
    def get_active_rental_for_place_id(self, place_id : str) -> Rental: 
        try:
            return next(r for r in self.get_rentals() if r.place_id == place_id and r.is_active() == True)
        except Exception:
            return None  
        
    def get_active_rentals_on_date(self, date: datetime) -> list: 
        return list(filter(lambda r: r.is_active_on_date(date) == True, self.get_rentals()))


    def save_rental(self, r: Rental) -> bool:
        try:
            with open(self.csv_file ,'a',newline='',encoding='utf-8') as f:
                writer = csv.writer(f)
                if os.path.getsize(self.csv_file) == 0:
                    writer.writerow(['licence_plate','name','place_id','rent_start','rent_end'])
                writer.writerow([
                    r.licence_plate, 
                    r.name, 
                    r.place_id, 
                    self._datetime_to_str(r.rent_start), 
                    self._datetime_to_str(r.rent_end)
                    ])
                self._rentals = None
            return True
        except Exception:
            logging.exception("Error saving rental to csv file")
            return False

    def delete_rentals(self) -> bool:
        try:
            self._delete_content()
            self._rentals = None
            return True
        except Exception:
            logging.exception("Error deleting rentals from csv file")
            return False

