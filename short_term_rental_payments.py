
from datetime import datetime
import os
import csv
import logging
from csv_service import BaseCsvService



class ShortTermRentalPayment:
  def __init__(self, place_id: str, licence_plate : str, amount : int, date : datetime = datetime.now()):
    self.licence_plate = licence_plate
    self.place_id = place_id
    self.amount = amount
    self.date = date
      
class ShortTermRentalPaymentService(BaseCsvService):
    def __init__(self, csv_file : str = 'csv/short_term_rental_payment.csv'):
        super().__init__(csv_file)
        self._payments : list = None
    
    def get_payments(self) -> list:
        if self._payments is not None :
            return self._payments

        self._payments = []
        try:
            with open(self.csv_file , mode='r', newline='',encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    place_id = row[0]
                    licence_plate =  row[1]
                    amount = self._str_to_int(row[2])
                    date = self._str_to_datetime(row[3])
                    self._payments.append(ShortTermRentalPayment(place_id, licence_plate, amount, date))
        except Exception:
            logging.exception("Error reading payment from csv file")
            pass
        return self._payments
    
    def save_payment(self, p: ShortTermRentalPayment) -> bool:
        try:
            with open(self.csv_file ,'a',newline='',encoding='utf-8') as f:
                writer = csv.writer(f)
                if os.path.getsize(self.csv_file) == 0:
                    writer.writerow(['place_id','licence_plate','amount','date'])
                writer.writerow([
                    p.place_id, 
                    p.licence_plate, 
                    self._int_to_str(p.amount),
                    self._datetime_to_str(p.date), 
                    ])
                self._payments = None
            return True
        except Exception:
            logging.exception("Error saving payment to csv file")
            return False

    def delete_payments(self) -> bool:
        try:
            self._delete_content()
            self._payments = None
            return True
        except Exception:
            logging.exception("Error deleting payments from csv file")
            return False