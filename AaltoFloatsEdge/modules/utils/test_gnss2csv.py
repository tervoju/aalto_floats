import time
import sys
import os
import logging
import json
import csv

from flatten_json import flatten
from datetime import datetime
from datetime import timezone

from gnss2csv import gnss2csv_file

gnss_json = {
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "GeopointTelemetry": {
        "lat": 60.9,
        "lon": 24.5,
        "alt": 23
    },
    "speed": 12.0,
    "deviceId": "Device",
    "machineId": 1121213
}

def test():
    print("gnss test")
    to_csv = gnss2csv_file
    to_csv.write_csv_data(gnss_json)

if __name__ == "__main":
    test()
