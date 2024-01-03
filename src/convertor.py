import pygrib
import xlsxwriter
from progress.bar import Bar
import time

# {self.date_instance.year}{self.date_instance.month}{int(self.date_instance.day)-1}

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










































    # def grib_convert(self, date_instance):
    #     self.date_instance = date_instance
    #     expenses = []
    #     index = 0
        
    #     grbs = pygrib.open(f'public/{date_instance.year}{date_instance.month}{int(date_instance.day)-1}/gfs.t18z.pgrb2.0p25.f000')  
    #     grb = grbs.read()
    #     lats, lons = grb.latlons()
            



    #     grb = grb[0]
  
        
    #     for _ in range(len(grb.values)):
    #         for _2 in range(len(grb.values[_])):
    #             print((lats[_][_2]), " ", (lons[_][_2]), " ", (grb.values[_][_2]))
    #             expenses.append([lats[_][_2], lons[_][_2], grb.values[_][_2]])
    #             index +=1
                
    #             if index == 300:
    #                 print(expenses)
    #                 print(len(expenses))
    #                 for _ in expenses:
    #                     print(len(_))
    #                     print((_))
                    
    #                 return {
    #                     "date_instance": date_instance,
    #                     "data": expenses
    #                 }


    # def convert_grib_data_to_xls(self, data: dict):
    #     workbook = xlsxwriter.Workbook(f"public/{self.date_instance.year}{self.date_instance.month}{int(self.date_instance.day)-1}/gfs.xlsx")
    #     worksheet = workbook.add_worksheet()


    #     row = 1
    #     col = 0

    #     worksheet.write(0, col,     "lat")
    #     worksheet.write(0, col + 1, "lon")
    #     worksheet.write(0, col + 2, "val")
    #     # Iterate over the data and write it out row by row.
    #     for _lat, _lon, _val in tuple(data["data"]):
    #         worksheet.write(row, col,     _lat)
    #         worksheet.write(row, col + 1, _lon)
    #         worksheet.write(row, col + 2, _val)
    #         row += 1

    #     workbook.close()