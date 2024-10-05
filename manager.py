import os
import sys
import subprocess
import threading
import requests
import datetime
import time
import json
import pandas as pd

server_status: str = "off"
# server_status: str = "ready"
# server_status: str = "working"


def run_server():
    os.system("docker compose up --build")

def update_data():
    if server_status == "ready":
        requests.get("http://127.0.0.1:5000/update/")
    time.sleep(5)

def convert_xlsx_to_csv():
    read_file = pd.read_excel ("final.xlsx")

    read_file.to_csv ("final.csv", 
        index = None, 
        header=True
    )


def main():
    threading.Thread(target=run_server).start()

    res_status_code = 0
    while not (res_status_code == 200):
        try:
            res = requests.get("http://127.0.0.1:5000/")
            res_status_code = res.status_code
        except: pass
        
        
    date = datetime.datetime.now() - datetime.timedelta(days=1)
    date_instance = date
    date = "{}{:0>2}{:0>2}".format(date.year, date.month, date.day)
    
    update_data()
    
    res = {
        "busy": True
    }
    while res['busy']:
        try:
            res = json.loads(
                requests.get(
                    "http://127.0.0.1:5000/status/"
                ).text
            )
            print(res)
        except: pass
    print(res)
    
    final_file = requests.get(
        "http://127.0.0.1:5000/download/?file-name=public/{}{:0>2}{:0>2}/gfs.xlsx".format(
            date_instance.year,
            date_instance.month,
            date_instance.day
            ),
        stream=True
    )
    f = open(f"final.xlsx", "wb")
    
    downloaded: int = 0
    for chunk in (final_file.iter_content(chunk_size=1024)): 
        if chunk:
            # print(f"downloaded: {downloaded/(1024*1024):.2f} MB", end="\r")
            # sys.stdout.flush()        
            
            downloaded += len(chunk)
            f.write(chunk)
            f.flush()
            
    print(f"downloaded: {downloaded/(1024*1024):.2f} MB")
    f.close()
    
    print("Convert to csv ...")
    convert_xlsx_to_csv()
    
    
if (__name__ == "__main__"):
    main()
    print("Done !! (final.csv & final.xlsx)")
    sys.exit()