import os

from os import getenv
from typing import BinaryIO
from azure.storage.blob import BlobServiceClient

AZURE_STORAGE_ACCOUNT_NAME="siloiotvqc"
AZURE_STORAGE_ACCOUNT_KEY="yFpDA3LiAZocCMc13VoZnH4/Z1dNtfzUfWYXsqOCwclmcLZuZCBlXQH53siG+ERzYGYq+vYwFLGj+AStjWxdUw=="
ENDPOINT_SUFFIX="core.windows.net"

LOCAL_LOG_PATH = "/app/logs"

AZURE_STORAGE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=siloiotvqc;AccountKey=yFpDA3LiAZocCMc13VoZnH4/Z1dNtfzUfWYXsqOCwclmcLZuZCBlXQH53siG+ERzYGYq+vYwFLGj+AStjWxdUw==;EndpointSuffix=core.windows.net"

#blob_service_client = BlobServiceClient.from_connection_string(getenv(AZURE_STORAGE_CONNECTION_STRING))

def upload_blob(filename: str, container: str, data: BinaryIO):
    try:
        blob_client = blob_service_client.get_blob_client(
            container=container, blob=filename)
        # Get full path to the file
        upload_file_path = os.path.join(LOCAL_LOG_PATH, file_name)
        with open(upload_file_path, "rb") as data:
            blob_client.upload_blob(data,overwrite=True)
 
        #blob_client.upload_blob(data)
        print("success")
    except Exception as e:
        print(e.message)

def download_blob(filename: str, container: str):
    try:
        blob_client = blob_service_client.get_blob_client(
            container=container, blob=filename)
        print(blob_client.download_blob().readall())
    except Exception as e:
        print(e.message)


def delete_blob(filename: str, container: str):
    try:
        blob_client = blob_service_client.get_blob_client(
            container=container, blob=filename)
        blob_client.delete_blob()

        print("success")
    except Exception as e:
        print(e.message)

def create_container(container: str):
    try:
        blob_service_client.create_container(container)
        print("success")
    except Exception as e:
        print(e.message)

def delete_container(container: str):
    try:
        blob_service_client.delete_container(container)
        print("success")
    except Exception as e:
        print(e.message)

def get_containers():
    try:
        containers = blob_service_client.list_containers()
        print([container.name for container in containers])
    except Exception as e:
        print(e.message)

def store_log_to_blob(blob_name: str, file_name: str):
    # get client
    try:
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
    except Exception as e:
        print(e.message)
    
    try:
        blob_client = blob_service_client.get_blob_client(blob_name, file_name)
        # Get full path to the file
        upload_file_path = os.path.join(LOCAL_LOG_PATH, file_name)
        with open(upload_file_path, "rb") as data:
            blob_client.upload_blob(data,overwrite=True)
        print("success")
    except Exception as e:
        print(e.message)



if __name__=="__main__":
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
    containers = blob_service_client.list_containers()
    print([container.name for container in containers])    
    try:
        blob_client = blob_service_client.get_blob_client("test", "gnss_logs.csv")
        # Get full path to the file
        upload_file_path = os.path.join(LOCAL_LOG_PATH, "gnss_logs.csv")
        with open(upload_file_path, "rb") as data:
            blob_client.upload_blob(data,overwrite=True)
 
        #blob_client.upload_blob(data)
        print("success")
    except Exception as e:
        print(e.message)
