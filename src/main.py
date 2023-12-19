from .fetch import Fetch
from .convertor import Convertor

class Main(object):
    def __init__(self):
        fetch = Fetch()
        convertor = Convertor()
        
        date_instance = fetch.update()
        converted_data = convertor.grib_convert(date_instance)
        convertor.convert_grib_data_to_xls(converted_data)
        