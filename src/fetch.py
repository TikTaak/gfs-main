        # res = requests.get("https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl?dir=%2Fgfs.20231217%2F18%2Fatmos&file=gfs.t18z.pgrb2.0p25.anl&all_var=on&all_lev=on&subregion=&toplat=40&leftlon=40&rightlon=65&bottomlat=20", stream=True)
import config
import requests
import datetime
import os
from clint.textui import progress

class Fetch(object):
    date = None
    date_instance = None
    url = None

    def __init__(self):
        self.url = config.GFS_LINK
        
    def save_update(self):
        res = requests.get(self.url, stream=True)
        print(res.status_code)
        f = open(f"public/{self.date}/gfs.t18z.pgrb2.0p25.f000", "wb")
        print(res.headers.get('content-length'))
        total_length = int(res.headers.get('content-length'))
        for chunk in progress.bar(res.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
            if chunk:
                f.write(chunk)
                f.flush()
        f.close()
        
    def update(self, force=False):
        date = datetime.datetime.now()
        self.date_instance = date
        self.date = f"{date.year}{date.month}{int(date.day)-1}"
        
        
        if (os.path.isfile(f'public/{self.date}/gfs.t18z.pgrb2.0p25.f000')) and (not force):
            return self.date_instance
        
        else:
            os.system(f"mkdir public/{self.date}")
            
            self.url = self.url.replace("{{year}}", str(date.year))
            self.url = self.url.replace("{{month}}", str(date.month))
            self.url = self.url.replace("{{day}}", str(date.day - 1))
            
            print(self.url)
            self.save_update()
            return self.date_instance
        
            
            
        
        
        
        

