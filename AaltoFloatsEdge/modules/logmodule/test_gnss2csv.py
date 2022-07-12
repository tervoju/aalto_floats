# Copyright (c) Juha Tervo
# 

import asyncio
import sys
import os

import logging
from gnss2csv import gnss2csv_file
import json

to_gnss_csv = gnss2csv_file('/home/pi/logs/')

to_gnss_csv.remove_old_logs("gnss")