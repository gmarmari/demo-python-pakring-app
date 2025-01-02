
from abc import ABC, abstractmethod
from datetime import datetime
import math
import re

from activities import Activity, ActivityService
from rentals import Rental, RentalService
from parking_spaces import ParkingSpaceOverview, ParkingSpaceService
from short_term_rental_payments import ShortTermRentalPayment, DaysTakings, ShortTermRentalPaymentService

class ParkingController: 
    def __init__(self, rental_service: RentalService = RentalService(), 
                 parking_space_service : ParkingSpaceService = ParkingSpaceService(),
                 activity_service : ActivityService = ActivityService(),
                 payment_service : ShortTermRentalPaymentService = ShortTermRentalPaymentService()):
      self._rental_service = rental_service
      self._parking_space_service = parking_space_service
      self._activity_service = activity_service
      self._payment_service = payment_service
      self.view : ParkingControllerView = None
    

    def handle_incoming_car(self, license_plate: str):
      if len(license_plate) == 0 :
          self.view.error_no_licence_plate()
          return
      
      active_activity = self._activity_service.get_active_activity_for_licence_plate(license_plate)
      if active_activity is not None :
         self.view.show_parking_place(license_plate, active_activity.place_id)
         return
      
      existing_rental = self._rental_service.get_active_rental_for_licence_plate(license_plate)
      if  existing_rental != None : 
        self._activity_service.save_activity(Activity(existing_rental.place_id, license_plate))
        self._parking_space_service.update_parking_space(existing_rental.place_id, False)
        self.view.show_parking_place(license_plate, existing_rental.place_id)
        return
      
      space = self._parking_space_service.get_next_free_short_term_space()
      if space is None : 
         self.view.error_no_short_term_place_available()
      else : 
         self._activity_service.save_activity(Activity(space.place_id, license_plate))
         self._parking_space_service.update_parking_space(space.place_id, False)
         self.view.show_parking_place(license_plate, space.place_id)    

    def handle_outgoing_car(self, license_plate: str):
        if len(license_plate) == 0 :
          self.view.error_no_licence_plate()
          return
        existing_rental = self._rental_service.get_active_rental_for_licence_plate(license_plate)
        if  existing_rental != None : 
            self.view.show_goodbye_message(license_plate)
            return
        
        active_activity = self._activity_service.get_active_activity_for_licence_plate(license_plate)
        if active_activity is None : 
           self.view.error_no_incoming_activity_found(license_plate)
           return
        
        datetime_out = datetime.now()
        self._activity_service.update_activity(license_plate, datetime_out)

        self._parking_space_service.update_parking_space(active_activity.place_id, True)

        time_diference = datetime_out - active_activity.datetime_in
        hours = math.ceil(time_diference.total_seconds() / 3600)
        amount = hours*2

        payment = ShortTermRentalPayment(active_activity.place_id, active_activity.licence_plate, amount, datetime_out)
        self._payment_service.save_payment(payment)


        self.view.show_goodbye_with_payment_message(license_plate, amount)

    
    def get_free_long_term_parking_spaces_for_dates(self, 
                                                    date_start_str :str = datetime.now().strftime("%d-%m-%Y"), 
                                                    date_end_str: str = datetime.now().strftime("%d-%m-%Y")) -> list:
        if self.is_invalid_date(date_start_str) or self.is_invalid_date(date_end_str):
            return []
        
        date_start = datetime.strptime(date_start_str, "%d-%m-%Y")
        date_end = datetime.strptime(date_end_str, "%d-%m-%Y")
        active_rentals_start = self._rental_service.get_active_rentals_on_date(date_start)
        active_rentals_end = self._rental_service.get_active_rentals_on_date(date_end)

        free_spaces = self._parking_space_service.get_long_term_parking_spaces()

        free_place_ids = list(map(lambda s: s.place_id, free_spaces))
        for r in active_rentals_start:
            if r.place_id in free_place_ids :
                free_place_ids.remove(r.place_id)
        for r in active_rentals_end:
            if r.place_id in free_place_ids :
                free_place_ids.remove(r.place_id)
        return free_place_ids
    
    def handle_create_rental(self, licence_plate: str, name: str, place_id: str, date_start_str: str, date_end_str: str) :
        if licence_plate is None or len(licence_plate) == 0 :
            self.view.error_no_licence_plate()
            return
        if name is None or len(name) == 0 :
            self.view.error_no_name()
            return
        if place_id is None or len(place_id) == 0 :
            self.view.error_no_place()
            return
        if self.is_invalid_date(date_start_str):
            self.view.error_invalid_start_date()
            return
        if self.is_invalid_date(date_end_str):
            self.view.error_invalid_end_date()
            return
        
        date_start = datetime.strptime(date_start_str, "%d-%m-%Y")
        date_end = datetime.strptime(date_end_str, "%d-%m-%Y")

        if date_start <= datetime.now() or date_end <= date_start:
            self.view.error_invalid_start_end_date()
            return
        
        if self._rental_service.get_active_rental_for_place_id(place_id) is not None:
            self.view.error_place_is_not_available_for_rental(place_id)
            return

        self._rental_service.save_rental(Rental(place_id, licence_plate, name, date_start, date_end))
        self.view.show_rental_saved()

    def get_todays_takings(self) -> DaysTakings :
        payments = self._payment_service.get_payments_for_today()
        total_amount = 0
        for p in payments :
            total_amount += p.amount
        return DaysTakings(payments, total_amount)

    def get_parking_spaces_overview(self) -> list:
        list = []
        parking_spaces =  self._parking_space_service.get_parking_spaces()
        for i in range(len(parking_spaces)):
            space = parking_spaces[i]
            row = (i // 2)
            column = 0
            if i // 2 != i /2 :
                column = 1

            background="lightblue"
            if space.long_term == True :
                background= "yellow"

            text = space.place_id
            if space.is_free == False :
                activity = self._activity_service.get_active_activity_for_place_id(space.place_id)
                if activity is not None :
                    text += " - " + activity.licence_plate
            list.append(ParkingSpaceOverview(text, background, row, column))
        return list
    
    def get_active_activities(self) : 
        return self._activity_service.get_active_activities()
    
    def get_free_parking_spaces(self) : 
        return self._parking_space_service.get_free_parking_spaces()

    def is_invalid_date(self, text):
        pattern = r"^(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])-(\d{4})$"
        return re.fullmatch(pattern, text) is None  
        
       





class ParkingControllerView:
    
    @abstractmethod
    def show_parking_place(self, license_plate, place_id):
        pass

    @abstractmethod
    def show_goodbye_message(self, license_plate):
        pass

    @abstractmethod
    def show_goodbye_with_payment_message(self, license_plate, amount: str):
        pass

    @abstractmethod
    def show_rental_saved(self):
        pass
        
    @abstractmethod
    def error_no_licence_plate(self):
        pass

    @abstractmethod
    def error_no_name(self):
        pass

    @abstractmethod
    def error_no_place(self):
        pass

    @abstractmethod
    def error_invalid_start_date(self):
        pass

    @abstractmethod
    def error_invalid_end_date(self):
        pass

    @abstractmethod
    def error_invalid_start_end_date(self):
        pass
    
    @abstractmethod
    def error_no_short_term_place_available(self):
        pass

    @abstractmethod
    def error_no_incoming_activity_found(self, license_plate):
        pass

    @abstractmethod
    def error_place_is_not_available_for_rental(self, place_id):
        pass
    
        
            
            








