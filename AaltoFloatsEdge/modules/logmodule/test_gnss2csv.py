# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

import asyncio
import sys
import os

import logging
from gnss2csv import gnss2csv_file
import json

to_gnss_csv = gnss2csv_file('/home/pi/logs/')

to_gnss_csv.remove_old_logs("gnss")