import os
import datetime
import requests
import pygrib
import xlsxwriter
from clint.textui import progress
from progress.bar import Bar

GFS_LINK: str = "https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl?dir=%2Fgfs.{{year}}{{month}}{{day}}%2F18%2Fatmos&file=gfs.t18z.pgrb2.0p25.f003&all_var=on&all_lev=on&subregion=&toplat=40&leftlon=40&rightlon=65&bottomlat=20"

class Convertor():
    date_instance = None

    def grib_convert(self, date_instance):
        self.date_instance = date_instance
        
        
        path = 'public/{}{:0>2}{:0>2}/gfs.t18z.pgrb2.0p25.f000'.format(
            self.date_instance.year, 
            self.date_instance.month, 
            self.date_instance.day
        )
        
        print(path)
        ogrb = pygrib.open(path)
        
        grbs = ogrb.read()
        lats, lons = grbs[0].latlons()


        ####### create zojmoratab ########
        zojmoratab = []
        for i in range(len(lats)):
            for j in range(len(lats[i])):
                zojmoratab.append([i, j])
                del j
            del i
        ##################################


        ####### create header ########
        header = ["lat", "lon"]
        for index, grb in enumerate(grbs):
            header.append(grb.name)
            del index
            del grb
        ##################################

        def zojmoratab_serializer(matrix: list):
            satr = []
            for k in zojmoratab:
                satr.append(matrix[k[0]][k[1]])
                del k
            return satr

        body=[]
        #####################
        satr_lan = zojmoratab_serializer(lats)
        satr_lon = zojmoratab_serializer(lons)
        ####################
        body.append(satr_lan)
        body.append(satr_lon)

        bar = Bar('load gribs', max=len(grbs))
        # _count = 0
        for grb in (grbs):
            body.append(zojmoratab_serializer(grb.values))
            # time.sleep(0.5)
            grb = None
            # _count+=1
            # print(f"{_count}/{len(grbs)}")
            bar.next()
        bar.finish()
        
        return {
            "date_instance": date_instance,
            "header": header,
            "body": body,
        }


    def convert_grib_data_to_xls(self, data: dict):
        header = data["header"]
        body = data["body"]
        date_instance = data["date_instance"]
        
        workbook = xlsxwriter.Workbook("public/{}{:0>2}{:0>2}/gfs.xlsx".format(
            self.date_instance.year,
            self.date_instance.month,
            self.date_instance.day
            ))
        worksheet = workbook.add_worksheet()
        
        for index, head in enumerate(header):
            worksheet.write(0, index, head)

        bar = Bar('serializing', max=len(body))
        for i, l in enumerate(body):
            for index, lan in enumerate(l):
                worksheet.write(
                    int(index+2),
                    int(i),
                    str(lan)
                )
            bar.next()
        bar.finish()

        workbook.close()
        print("created")    



class Fetch(object):
    date = None
    date_instance = None
    url = None

    def __init__(self):
        self.url = GFS_LINK
        
        
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
        print(res.status_code)
        f = open(f"public/{self.date}/gfs.t18z.pgrb2.0p25.f000", "wb")
        print(res.headers.get('content-length'))
        total_length = int(res.headers.get('content-length'))
        for chunk in progress.bar(res.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
            if chunk:
                f.write(chunk)
                f.flush()
        f.close()
            






class Main(object):
    def __init__(self):
        fetch = Fetch()
        convertor = Convertor()
        
        date_instance = fetch.update()
        converted_data = convertor.grib_convert(date_instance)
        convertor.convert_grib_data_to_xls(converted_data)
        

