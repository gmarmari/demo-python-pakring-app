
from abc import ABC, abstractmethod
from datetime import datetime
import math

from activities import Activity, ActivityService
from rentals import RentalService
from parking_spaces import ParkingSpaceService
from short_term_rental_payments import ShortTermRentalPayment, ShortTermRentalPaymentService

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
    def error_no_licence_plate(self):
        pass
    
    @abstractmethod
    def error_no_short_term_place_available(self):
        pass

    @abstractmethod
    def error_no_incoming_activity_found(self, license_plate):
        pass
    
        
            
            








