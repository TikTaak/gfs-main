        # res = requests.get("https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl?dir=%2Fgfs.20231217%2F18%2Fatmos&file=gfs.t18z.pgrb2.0p25.anl&all_var=on&all_lev=on&subregion=&toplat=40&leftlon=40&rightlon=65&bottomlat=20", stream=True)
import config
import requests
import datetime
import os
from clint.textui import progress
import sys

class Fetch(object):
    date = None
    date_instance = None
    url = None

    def __init__(self):
        self.url = config.GFS_LINK
        
        
    def update(self, force=False):
        date = datetime.datetime.now() - datetime.timedelta(days=1)
        self.date_instance = date
        print(self.date_instance)
        self.date = "{}{:0>2}{:0>2}".format(date.year, date.month, date.day)
        print(self.date)
        
        
        if (os.path.isfile(f'public/{self.date}/gfs.t18z.pgrb2.0p25.f000')) and (not force):
            return self.date_instance
        
        else:
            os.system(f"mkdir public/{self.date}")
            
            self.url = self.url.replace("{{year}}", str(date.year))
            self.url = self.url.replace("{{month}}", "{:0>2}".format(str(date.month)))
            self.url = self.url.replace("{{day}}", "{:0>2}".format(str(date.day)))
            
            print(self.url)
            self.save_update()
            return self.date_instance
        
    def save_update(self):
        res = requests.get(self.url, stream=True)
        print(f"{res.status_code = }")
        f = open(f"public/{self.date}/gfs.t18z.pgrb2.0p25.f000", "wb")
        
        downloaded: int = 0
        for chunk in (res.iter_content(chunk_size=1024)): 
            if chunk:
                # print(f"downloaded: {downloaded/(1024*1024):.2f} MB", end="\r")
                # sys.stdout.flush()        
                
                downloaded += len(chunk)
                f.write(chunk)
                f.flush()
                
        print(f"downloaded: {downloaded/(1024*1024):.2f} MB")
        f.close()
            
            
        
        
        
        

