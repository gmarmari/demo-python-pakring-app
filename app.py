import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from datetime import datetime

from controller import ParkingController
from controller import ParkingControllerView

from short_term_rental_payments import DaysTakings

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

        self.licence_plate_entry = None
        self.name_entry = None
        self.parking_place_compobox = None
        self.date_start_entry = None
        self.date_end_entry = None

        self._create_menu_options()

    def _create_menu_options(self):  
        incoming_car_button = tk.Button(self.menu_frame, width=15, text=TEXT_INCOMING_CAR,command=self._open_detail_incoming_car)  
        incoming_car_button.grid(row=0,column=0,padx=5,pady=5)

        outgoung_car_button = tk.Button(self.menu_frame, width=15, text=TEXT_OUTGOING_CAR,command=self._open_detail_outgoing_car)  
        outgoung_car_button.grid(row=1,column=0,padx=5,pady=5)

        long_term_rental_button = tk.Button(self.menu_frame, width=15, text=TEXT_LONG_TERM_RENTAL,command=self._open_detail_create_long_term_rental)  
        long_term_rental_button.grid(row=2,column=0,padx=5,pady=5)

        days_takings_button = tk.Button(self.menu_frame, width=15, text=TEXT_DAYS_TAKINGS,command=self._open_detail_days_takings)  
        days_takings_button.grid(row=3,column=0,padx=5,pady=5)

        parking_spaces_button = tk.Button(self.menu_frame, width=15, text=TEXT_PARKING_SPACES,command=self._open_detail_parking_spaces)  
        parking_spaces_button.grid(row=4,column=0,padx=5,pady=5)

        parked_cars_button = tk.Button(self.menu_frame, width=15, text=TEXT_PARKED_CARS,command=self._open_detail_parked_cars)  
        parked_cars_button.grid(row=5,column=0,padx=5,pady=5)

        free_parking_spaces_button = tk.Button(self.menu_frame, width=15, text=TEXT_FREE_PARKING_SPACES,command=self._open_detail_free_parking_spaces)  
        free_parking_spaces_button.grid(row=6,column=0,padx=5,pady=5)

        total_takings_button = tk.Button(self.menu_frame, width=15, text=TEXT_TOTAL_TAKINGS,command=self._open_detail_total_takings)  
        total_takings_button.grid(row=7,column=0,padx=5,pady=5)

        


    
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

    def _open_detail_create_long_term_rental(self):
        self._clear_detail_frame()
        title_label = tk.Label(self.detail_frame,text=TEXT_LONG_TERM_RENTAL)
        title_label.grid(row=0,column=0,columnspan=3, padx=10,pady=5)  

        licence_plate_label = tk.Label(self.detail_frame,text=LABEL_LICENCE_PLATE)
        licence_plate_label.grid(row=1,column=0,padx=10,pady=5)  

        self.licence_plate_entry = tk.Entry(self.detail_frame, width=50)
        self.licence_plate_entry.grid(row=1,column=1,padx=10,pady=5)  

        name_label = tk.Label(self.detail_frame,text=LABEL_NAME)
        name_label.grid(row=2,column=0,padx=10,pady=5)  

        self.name_entry = tk.Entry(self.detail_frame, width=50)
        self.name_entry.grid(row=2,column=1,padx=10,pady=5)    

        start_label = tk.Label(self.detail_frame,text=LABEL_START)
        start_label.grid(row=3,column=0,padx=10,pady=5)  

        current_date = datetime.now().strftime("%d-%m-%Y")
    
        self.date_start_entry = tk.Entry(self.detail_frame, width=50)
        self.date_start_entry.grid(row=3,column=1,padx=10,pady=5) 
        self.date_start_entry.insert(0, current_date)
        self.date_start_entry.bind("<FocusOut>", self._on_date_entry_focus_out_event)

        end_label = tk.Label(self.detail_frame,text=LABEL_END)
        end_label.grid(row=4,column=0,padx=10,pady=5)  
    
        self.date_end_entry = tk.Entry(self.detail_frame, width=50)
        self.date_end_entry.grid(row=4,column=1,padx=10,pady=5)  
        self.date_end_entry.insert(0, current_date)
        self.date_end_entry.bind("<FocusOut>", self._on_date_entry_focus_out_event)

        parking_place_label = tk.Label(self.detail_frame,text=LABEL_PLACE)
        parking_place_label.grid(row=5,column=0,padx=10,pady=5)  

        list = self.controller.get_free_long_term_parking_spaces_for_dates()
        self.parking_place_compobox = ttk.Combobox(self.detail_frame, values=list, state="readonly", width=50)
        if len(list) > 0 :
            self.parking_place_compobox.set(list[0])
        else:
            self.parking_place_compobox.set("")
        self.parking_place_compobox.grid(row=5, column=1, padx=10,pady=5) 

        ok_button = tk.Button(self.detail_frame, text=TEXT_OK,command=self._handle_create_long_term_rental)  
        ok_button.grid(row=6,column=3,padx=5,pady=5)


    def _open_detail_days_takings(self) : 
        self._clear_detail_frame()

        title_label = tk.Label(self.detail_frame,text=TEXT_DAYS_TAKINGS)
        title_label.grid(row=0,column=0,columnspan=3, padx=10,pady=5)  

        columns = (TEXT_LICENCE_PLATE, TEXT_PLACE, TEXT_DATE, TEXT_AMOUNT_IN_EURO)
        tree = ttk.Treeview(self.detail_frame, columns=columns, show='headings')

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)

        takings = self.controller.get_todays_takings()
        for p in takings.payments:
            tree.insert('', tk.END, values=(p.licence_plate, p.place_id, p.date_to_string(), p.amount))
        tree.grid(row=1, column=0,padx=10,pady=5)  

        sum_label = tk.Label(self.detail_frame,text=LABEL_TOTAL_AMOUNT + " " + str(takings.total_amount))
        sum_label.grid(row=2,column=0,padx=10,pady=5)  


    def _open_detail_parking_spaces(self) :
        self._clear_detail_frame()

        title_label = tk.Label(self.detail_frame,text=TEXT_PARKING_SPACES)
        title_label.grid(row=0,column=0,columnspan=3, padx=10,pady=5)  

        parking_spaces = self.controller.get_parking_spaces_overview()
        for p in parking_spaces :
            label = tk.Label(self.detail_frame,text=p.text, width=20, bg=p.background)
            label.grid(row=p.row+1,column=p.column, padx=10,pady=10)  

    def _open_detail_parked_cars(self) : 
        self._clear_detail_frame()

        title_label = tk.Label(self.detail_frame,text=TEXT_PARKED_CARS)
        title_label.grid(row=0,column=0,columnspan=3, padx=10,pady=5)  

        columns = (TEXT_LICENCE_PLATE, TEXT_PLACE, TEXT_DATE_IN)
        tree = ttk.Treeview(self.detail_frame, columns=columns, show='headings')

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)

        activities = self.controller.get_active_activities()
        for a in activities:
            tree.insert('', tk.END, values=(a.licence_plate, a.place_id, a.datetime_in_to_string()))
        tree.grid(row=1, column=0,padx=10,pady=5)  


    def _open_detail_free_parking_spaces(self) : 
        self._clear_detail_frame()

        title_label = tk.Label(self.detail_frame,text=TEXT_FREE_PARKING_SPACES)
        title_label.grid(row=0,column=0,columnspan=3, padx=10,pady=5)  

        columns = (TEXT_PLACE, TEXT_LONG_TERM)
        tree = ttk.Treeview(self.detail_frame, columns=columns, show='headings')

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)

        parking_spaces = self.controller.get_free_parking_spaces()
        for p in parking_spaces:
            long_term = TEXT_NO
            if p.long_term == True :
                long_term = TEXT_YES
            tree.insert('', tk.END, values=(p.place_id, long_term))
        tree.grid(row=1, column=0,padx=10,pady=5)  

    def _open_detail_total_takings(self) :
        self._clear_detail_frame()

        title_label = tk.Label(self.detail_frame,text=TEXT_TOTAL_TAKINGS)
        title_label.grid(row=0,column=0,columnspan=3, padx=10,pady=5)  

        columns = (TEXT_LICENCE_PLATE, TEXT_AMOUNT_IN_EURO)
        tree = ttk.Treeview(self.detail_frame, columns=columns, show='headings')

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)

        total_takings = self.controller.get_total_takings()
        for t in total_takings:
            tree.insert('', tk.END, values=(t.licence_plate, t.amount))
        tree.grid(row=1, column=0,padx=10,pady=5)  


        


    def _on_date_entry_focus_out_event(self, event):
        list = self.controller.get_free_long_term_parking_spaces_for_dates(
                self._get_entry_text(self.date_start_entry), 
                self._get_entry_text(self.date_end_entry))
            
        if len(list) == 0 :
            messagebox.showerror(message=ERROR_NO_PLACE_AVAILABLE_FOR_RENTAL_ON_SELECTED_DATES)
        else:
            self.parking_place_compobox['values'] = list
            self.parking_place_compobox.set(list[0])




    def _handle_incoming_car(self): 
        self.controller.handle_incoming_car(self._get_entry_text(self.licence_plate_entry))

    def _handle_outgoing_car(self): 
        self.controller.handle_outgoing_car(self._get_entry_text(self.licence_plate_entry))

    def _handle_create_long_term_rental(self): 
        self.controller.handle_create_rental(
            self._get_entry_text(self.licence_plate_entry),
            self._get_entry_text(self.name_entry),
            self.parking_place_compobox.get(),
            self._get_entry_text(self.date_start_entry),
            self._get_entry_text(self.date_end_entry)
        )

    def _clear_detail_frame(self):
        for widget in self.detail_frame.winfo_children():
            widget.destroy()
        self.licence_plate_entry = None
        self.name_entry = None
        self.parking_place_compobox = None
        self.date_start_entry = None
        self.date_end_entry = None
    
    def _clear_licence_plate_entry(self):
        if self.licence_plate_entry is not None :
            self.licence_plate_entry.delete(0, tk.END)
    
    def _get_entry_text(self, enty: tk.Entry):
        text =  enty.get()
        if text is None : 
            return ""
        else:
            return text.strip()
    







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

    def show_rental_saved(self):
        messagebox.showinfo(message = TEXT_RENTAL_SAVED)

    def error_no_licence_plate(self):
        messagebox.showerror(message = ERROR_NO_LICENCE_PLATE)

    def error_no_name(self):
        messagebox.showerror(message = ERROR_NO_NAME)

    def error_no_place(self):
        messagebox.showerror(message = ERROR_NO_PLACE)

    def error_invalid_start_date(self):
        messagebox.showerror(message = ERROR_INVALID_START_DATE)
    
    def error_invalid_end_date(self):
        messagebox.showerror(message = ERROR_INVALID_END_DATE)

    def error_invalid_start_end_date(self):
        messagebox.showerror(message = ERROR_INVALID_START_END_DATE)

    def error_no_short_term_place_available(self):
        messagebox.showerror(message = ERROR_SHORT_TERM_PLACE_AVAILABLE)

    def error_no_incoming_activity_found(self, license_plate):
        messagebox.showerror(message = ERROR_NO_INCOMING_ACTIVITY_FOUND_FOR + " " + license_plate)

    def error_place_is_not_available_for_rental(self, place_id):
        messagebox.showerror(message = ERROR_PLACE_NOT_AVAILABLE_FOR_RENTAL + " " + place_id)


if __name__=='__main__':        
    root = tk.Tk()           
    controller = ParkingController()  
    view = ParkingApp(root, controller)
    controller.view = view
    root.mainloop()  





 

