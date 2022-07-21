import os
import sys
import logging

#global settings for ADC samples
PAUSE = 0
TWIN_CALLBACKS = 0
NRO_ADC_OF_MEASUREMENTS = 2000000
LOG_PATH = '/home/pi/logs/'

def get_ADC_samples(samples, pause):
    cmd = 'sudo /home/pi/hydro/rawMCP3202 2000000 0'
    so = os.popen(cmd).read()
    print(so)

get_ADC_samples(NRO_ADC_OF_MEASUREMENTS, PAUSE)


## check if there is change in file and request to do ADC

## loop to get ADC samples and store them to /home/pi/logs

##  change file to DONE
