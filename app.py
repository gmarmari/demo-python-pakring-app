import tkinter as tk
from tkinter import messagebox

from controller import ParkingController
from controller import ParkingControllerView

from messages import *

class ParkingApp(ParkingControllerView):
    def __init__(self,root, controller : ParkingController): 
        self.root = root
        self.controller = controller
        self.root.title(APP_TITLE)
        self.root.geometry("800x600")

        self.menu_frame = tk.Frame(self.root, width=200, bg="white")
        self.menu_frame.pack(side="left", fill="y")
        self.menu_frame.pack(padx=10,pady=10)

        self.detail_frame = tk.Frame(self.root, bg="white")
        self.detail_frame.pack(side="right", expand=True, fill="both")

        self._create_menu_options()

    def _create_menu_options(self):  
        incoming_car_button = tk.Button(self.menu_frame, text=TEXT_INCOMING_CAR,command=self._open_detail_incoming_car)  
        incoming_car_button.grid(row=0,column=0,padx=5,pady=5)

        outgoung_car_button = tk.Button(self.menu_frame, text=TEXT_OUTGOING_CAR,command=self._open_detail_outgoing_car)  
        outgoung_car_button.grid(row=1,column=0,padx=5,pady=5)

        
    
    def _open_detail_incoming_car(self):    
        self._clear_detail_frame()
        title_label = tk.Label(self.detail_frame,text=TEXT_INCOMING_CAR)
        title_label.grid(row=0,column=0,columnspan=3, padx=10,pady=5)  

        licence_plate_label = tk.Label(self.detail_frame,text=LABEL_LICENCE_PLATE)
        licence_plate_label.grid(row=1,column=0,padx=10,pady=5)  

        self.licence_plate_entry = tk.Entry(self.detail_frame, width=50)
        self.licence_plate_entry.grid(row=1,column=1,padx=10,pady=5)  

        ok_button = tk.Button(self.detail_frame, text=TEXT_OK,command=self._handle_incoming_car)  
        ok_button.grid(row=1,column=2,padx=5,pady=5)

    def _handle_incoming_car(self): 
        self.controller.handle_incoming_car(self._get_licence_plate())

    def _open_detail_outgoing_car(self):
        self._clear_detail_frame()
        title_label = tk.Label(self.detail_frame,text=TEXT_OUTGOING_CAR)
        title_label.grid(row=0,column=0,columnspan=3, padx=10,pady=5)  

        licence_plate_label = tk.Label(self.detail_frame,text=LABEL_LICENCE_PLATE)
        licence_plate_label.grid(row=1,column=0,padx=10,pady=5)  

        self.licence_plate_entry = tk.Entry(self.detail_frame, width=50)
        self.licence_plate_entry.grid(row=1,column=1,padx=10,pady=5)  

        ok_button = tk.Button(self.detail_frame, text=TEXT_OK,command=self._handle_outgoing_car)  
        ok_button.grid(row=1,column=2,padx=5,pady=5)

    def _handle_outgoing_car(self): 
        self.controller.handle_outgoing_car(self._get_licence_plate())

    def _clear_detail_frame(self):
        for widget in self.detail_frame.winfo_children():
            widget.destroy()
        self.licence_plate_entry = None
    
    def _clear_licence_plate_entry(self):
        if self.licence_plate_entry is not None :
            self.licence_plate_entry.delete(0, tk.END)

    def _get_licence_plate(self):
        license_plate =  self.licence_plate_entry.get()
        if license_plate is None : 
            return ""
        else:
            return license_plate.strip()







    # ParkingControllerView implementation

    def show_parking_place(self, license_plate, place_id):
        self._clear_licence_plate_entry()
        messagebox.showinfo(message = TEXT_WELLCOME + " " + license_plate + ". " + TEXT_YOUR_PARKING_PLACE + place_id + ".")
    
    def show_goodbye_message(self, license_plate):
        self._clear_licence_plate_entry()
        messagebox.showinfo(message = TEXT_GOODBYE + " " + license_plate)

    def show_goodbye_with_payment_message(self, license_plate, amount: str):
        self._clear_licence_plate_entry()
        messagebox.showinfo(message = TEXT_GOODBYE + " " + license_plate + ". " + TEXT_YOUR_PAYMENT + ": " + str(amount) + " " + CURRENCY)

    def error_no_licence_plate(self):
        messagebox.showerror(message = ERROR_NO_LICENCE_PLATE)

    def error_no_short_term_place_available(self):
        messagebox.showerror(message = ERROR_SHORT_TERM_PLACE_AVAILABLE)

    def error_no_incoming_activity_found(self, license_plate):
        messagebox.showerror(message = ERROR_NO_INCOMING_ACTIVITY_FOUND_FOR + " " + license_plate)


if __name__=='__main__':        
    root = tk.Tk()           
    controller = ParkingController()  
    view = ParkingApp(root, controller)
    controller.view = view
    root.mainloop()  





 

