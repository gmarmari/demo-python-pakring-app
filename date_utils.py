from datetime import datetime

class DateUtils:
    def __init__(self):
       pass

    def months_difference(self, start_date : datetime, end_date : datetime):
        """
        Calculates the difference in months between two dates""" 
        return (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)