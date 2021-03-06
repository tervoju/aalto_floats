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

AZURE_STORAGE_ACCOUNT_NAME=os.environ["AZURE_STORAGE_ACCOUNT_NAME"] 
AZURE_STORAGE_ACCOUNT_KEY=os.environ["AZURE_STORAGE_ACCOUNT_KEY"]
ENDPOINT_SUFFIX=os.environ["ENDPOINT_SUFFIX"]

LOCAL_LOG_PATH = "/app/logs"
AZURE_STORAGE_CONNECTION_STRING='DefaultEndpointsProtocol=https;AccountName=' + str(AZURE_STORAGE_ACCOUNT_NAME) + ';AccountKey=' + str(AZURE_STORAGE_ACCOUNT_KEY) +';EndpointSuffix='+ str(ENDPOINT_SUFFIX)
blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)

# blob storage upload
def store_log_to_blob(blob_name, file_name):
    logging.info('{}:{}'.format(blob_name, file_name))
    try:
        blob_client = blob_service_client.get_blob_client(blob_name, file_name)
        # Get full path to the file
        upload_file_path = os.path.join(LOCAL_LOG_PATH, file_name)
        with open(upload_file_path, "rb") as data:
            blob_client.upload_blob(data,overwrite=True)
        logging.info("loading file to blob success")

    except Exception as e:
        print(e.message)

# local log file
class gnss2csv_file:
    def __init__(self, log_path):
        #GNSS
        timestr = time.strftime("%Y%m%d-%H%M%S")
        csv_header_gnss = ['timestamp','datetime','lat','lon','alt','speed','fom','deviceId','machineId']
        self.log_path = log_path
        self.file_name = timestr + '_gnss_data.csv'
        self.csv_file_gnss = open(log_path + timestr + '_gnss_data.csv', 'w')
        print(self.file_name)
        print(self.csv_file_gnss.name)
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

    def remove_old_logs(self, type):
        log_files = self.log_path 
        logging.info("{}:{}".format("removing old logs", type))
        logging.info("{}:{}".format("log_files", log_files))
        try:
            filenames = [entry.name for entry in sorted(os.scandir(log_files),
                key=lambda x: x.stat().st_mtime, reverse=True)]
            # saves last two files
            for filename in filenames[2:]:
                filename_relPath = os.path.join(self.log_path, filename)
                if filename_relPath.__contains__(type):
                    os.remove(filename_relPath)
        except Exception as ex:
            logging.info("{}:{}".format("Unexpected error in twin_patch_listener", ex ))

    
    def close_csv_log(self):
        file_name = self.file_name
        self.csv_file_gnss.close() # when you're done.
        #write file to blob - trial
        logging.info('{}:{}'.format("file to blob", file_name))
        store_log_to_blob("gnsslogs", file_name)


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
