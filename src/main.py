from .fetch import Fetch
from .convertor import Convertor
from dataclasses import dataclass


class Main(object):
    busy: bool = False
    status: str = None
    
    @dataclass
    class statuses:
        fetch = "fetching"
        convert_grib = "convert grib"
        idle = "idle"
    
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Main, cls).__new__(cls)
        return cls.instance
    
    def __init__(self):
        pass
    
    def do_progress(self, force=False) -> None:
        if not self.busy:
            self.busy = True  

            fetch = Fetch()
            convertor = Convertor()
            self.status = self.statuses.fetch
            print(f"{self.status = }")
            date_instance = fetch.update(force=force)
            
            self.status = self.statuses.convert_grib
            print(f"{self.status = }")
            converted_data = convertor.grib_convert(date_instance)
            convertor.convert_grib_data_to_xls(converted_data)
            
            self.status = self.statuses.idle
            print(f"{self.status = }")
            self.busy = False
        return None
        
        