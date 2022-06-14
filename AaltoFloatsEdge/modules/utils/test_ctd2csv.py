import time
import sys
import os
import logging
import json
import csv

from flatten_json import flatten
from datetime import datetime
from datetime import timezone

from ctd2csv import ctd2csv_file



def test():
    print("ctd test")
    to_csv = ctd2csv_file()
    to_csv.write_csv_data(23.0, 15.0, 10.0, "device","machine")

if __name__ == "__main__":
    test()


# b'$AQCTD,23.268,01.012,-00.000*53\r'