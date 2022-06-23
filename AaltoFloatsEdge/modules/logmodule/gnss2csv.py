import time
import sys
import os
import logging
import json
import csv

from flatten_json import flatten
from datetime import datetime
from datetime import timezone

from os import getenv
from typing import BinaryIO
from venv import create
from azure.storage.blob import BlobServiceClient

AZURE_STORAGE_ACCOUNT_NAME="siloiotvqc"
AZURE_STORAGE_ACCOUNT_KEY="yFpDA3LiAZocCMc13VoZnH4/Z1dNtfzUfWYXsqOCwclmcLZuZCBlXQH53siG+ERzYGYq+vYwFLGj+AStjWxdUw=="
ENDPOINT_SUFFIX="core.windows.net"

LOCAL_LOG_PATH = "/app/logs"
AZURE_STORAGE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=siloiotvqc;AccountKey=yFpDA3LiAZocCMc13VoZnH4/Z1dNtfzUfWYXsqOCwclmcLZuZCBlXQH53siG+ERzYGYq+vYwFLGj+AStjWxdUw==;EndpointSuffix=core.windows.net"


blob = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)

def store_log_to_blob(self, blob_name: str, file_name: str):
    global blob
    try:
        blob_client = blob_service_client.get_blob_client(blob_name, file_name)
        # Get full path to the file
        upload_file_path = os.path.join(LOCAL_LOG_PATH, file_name)
        with open(upload_file_path, "rb") as data:
            blob_client.upload_blob(data,overwrite=True)
        print("success")

    except Exception as e:
        print(e.message)


class gnss2csv_file:
    def __init__(self):
        #GNSS
        timestr = time.strftime("%Y%m%d-%H%M%S")
        csv_header_gnss = ['timestamp','datetime','lat','lon','alt','speed','fom','deviceId','machineId']
        self.file_name = timestr + '_gnss_data.csv'
        self.csv_file_gnss = open('./logs/' + timestr + '_gnss_data.csv', 'w')
        self.csv_writer_gnss = csv.writer(self.csv_file_gnss)
        self.csv_writer_gnss.writerow(csv_header_gnss)
        self.csv_file_gnss.flush() 

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
    
    def close_csv_log(self):
        global blob
        self.csv_file_gnss.close() # when you're done.
        #write file to blob?
        blob.store_log_to_blob("gnsslogs", self.file_name)


    def write_csv_data(self, gnss_jsondata):
        try:
            # ct stores current time
            ct = datetime.now()
            # ts store timestamp of current time
            ts = ct.timestamp()            
            csv_s = flatten(gnss_jsondata)
            csv_data = self.generate_csv_data(csv_s)
            csv_rows = csv_data.split('\n')
            if csv_rows[1]:
                gnss_array = csv_rows[1].split(',')
                gnss_array.insert(0, ts)  
                self.csv_writer_gnss.writerow(gnss_array)
                self.csv_file_gnss.flush() 

        except:
            logging.info('fails to write csv')
