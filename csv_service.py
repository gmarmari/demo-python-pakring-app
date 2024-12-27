from datetime import datetime

class BaseCsvService:
    def __init__(self, csv_file: str):
        self.csv_file = csv_file 
        self._datetime_format = "%Y-%m-%d %H:%M:%S"

    def _delete_content(self): 
        with open(self.csv_file ,'a',newline='',encoding='utf-8') as f:
            f.truncate(0) # Deletes all content

    def _datetime_to_str(self, dt: datetime = None) -> str:
      if dt is None :
         return ""
      else :
        return dt.strftime(self._datetime_format)
    
    def _str_to_datetime(self, dt_string: str) -> datetime:
        if dt_string is None or dt_string == "":
           return None
        else :
          return datetime.strptime(dt_string, self._datetime_format)

    def _bool_to_str(self, bool_value: bool) -> str:
        return str(bool_value)
        
    def _str_to_bool(self, bool_str: str) -> bool:
        return bool_str.lower() == 'true'
    
    def _int_to_str(self, int_value : int) -> str :
        return str(int_value)
    
    def _str_to_int(self, int_str: str) -> int:
        return int(int_str)