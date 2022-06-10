import logging
import time
from datetime import datetime

from logging.handlers import RotatingFileHandler
 
# create log file
def create_rotating_file(path, maxsize):
    logger = logging.getLogger("Rotating Log")
    logger.setLevel(logging.INFO)   
    # add a rotating handler
    handler = RotatingFileHandler(path, maxBytes=1000, backupCount=1)
    logger.addHandler(handler)
    return logger

# add log line to file
def add_ring_logging(logger, dt, csv_str):
    # Append text at the end of file
    str_str = str(dt) + " "  + csv_str  
    logger.info(str_str)
         