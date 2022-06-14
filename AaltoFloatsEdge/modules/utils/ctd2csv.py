import time
import sys
import os
import logging
import json
import csv

from flatten_json import flatten
from datetime import datetime
from datetime import timezone
 
 # b'$AQCTD,23.268,01.012,-00.000*53\r'

class ctd2csv_file:
    def __init__(self):
        #CTD
        timestr = time.strftime("%Y%m%d-%H%M%S")
        csv_header_ctd = ['timestamp','datetime','C','T','D','deviceId','machineId']
        csv_file_ctd = open(timestr + '_ctd_data.csv', 'w')
        self.csv_writer_ctd = csv.writer(csv_file_ctd)
        self.csv_writer_ctd.writerow(csv_header_ctd)

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

    def write_csv_data(self, temperature, pressure, conductivity, deviceId, machineId):
        try:
            # ct stores current time
            ct = datetime.now()
            # ts store timestamp of current time
            ts = ct.timestamp()                  
            ctd_array = []
            ctd_array.append(ts)  
            ctd_array.append(conductivity)  
            ctd_array.append(temperature)  
            ctd_array.append(pressure)  
            ctd_array.append(deviceId)
            ctd_array.append(machineId)
            print(ctd_array)
            self.csv_writer_ctd.writerow(ctd_array)

        except:
            logging.info('fails to write csv')
