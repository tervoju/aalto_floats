import time
import sys
import os
import logging
import json
import csv

from flatten_json import flatten
from datetime import datetime
from datetime import timezone
 

class gnss2csv_file:
    def __init__(self):
        #GNSS
        timestr = time.strftime("%Y%m%d-%H%M%S")
        csv_header_gnss = ['timestamp','lat','lon','alt','speed','fom','deviceId','machineId']
        csv_file_gnss = open(timestr + 'gnss_data.csv', 'w')
        self.csv_writer_gnss = csv.writer(csv_file_time)

    def generate_csv_data(self, data: dict) -> str:
        # Defining CSV columns in a list to maintain
        # the order
        csv_columns = data.keys()
  
        # Generate the first row of CSV 
        csv_data = ",".join(csv_columns) + "\n"
  
        # Generate the single record present
        new_row = list()
        for col in csv_columns:
            new_row.append(str(data[col]))
  
        # Concatenate the record with the column information 
        # in CSV format
        csv_data += ",".join(new_row) + "\n"
        return csv_data

    def write_csv_data(self, dvl_jsondata):
        try:
            # ct stores current time
            ct = datetime.now()
            # ts store timestamp of current time
            ts = ct.timestamp()            
            csv_s = flatten(dvl_jsondata)
            csv_data = self.generate_csv_data(csv_s)
            csv_rows = csv_data.split('\n')
            if csv_rows[1]:
                dvl_array = csv_rows[1].split(',')
                dvl_array.insert(0, ts)  
                self.csv_writer_time.writerow(dvl_array)

        except:
            logging.info('fails to write csv')
