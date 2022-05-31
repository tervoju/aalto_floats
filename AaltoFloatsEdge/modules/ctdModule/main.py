# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

import asyncio
import sys
import signal
import threading
from azure.iot.device.aio import IoTHubModuleClient

import time
import serial
import sys
import binascii
import inspect
import codecs
import math
import pynmea2

atm_surface_pressure = 1.101325
lattitude = 59.8443631

# this is the device id connected through usb - serial convertion box
# ser = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=3.0)

# $  A  Q  C  T  D  
# in hex:
#  24 41 51 43 54 44 2c 32 33 2e 32 34 382c30312e3031302c30302e3030342a37410d0a
# example of CTD message
# b'$AQCTD,23.268,01.012,-00.000*53\r'

## intepredign string from CTD
def read_ctd_values(ctd_response):
    print ("response:", ctd_response)
    result = ctd_response.find('$AQCTD')
    conductivity = 0.0
    if result == -1:
        print("CTD start string not found")
        return -1,0,0,0
    try:
        values = ctd_response.split(',')
        print(values)
        temperature = float(values[1])
        pressure = float(values[2])
        tmp_conductivity = values[3].replace('\r', '')
        if tmp_conductivity.find('*'):
            split_conductivity = tmp_conductivity.split('*')
            conductivity = float(split_conductivity[0])
        else:
            conductivity = 0.1 # has to be checked the values
        return 0, temperature, pressure, conductivity
    except:
        print("fails to extract CTD values")
        return -1,0,0,0
    

# depth calculation based on previous algorithms in file ctd.c
# includes few magic numbers. TBD clarified
# TODO: magic numbers

def calc_depth(pres, lat ):
    global atm_surface_pressure

	#actually measure & record atmospheric surface pressure
    pres = ( pres - atm_surface_pressure ) * 10 # from bar absolute pressure to decibar gauge pressure
	
    if pres < 0:
        return -1

	# FIXME: assume much lower salinity
    specific_volume = pres * ( 9.72659 + pres * ( -2.2512e-5 + pres * ( 2.279e-10 + pres * -1.82e-15 ) ) )
    
    s = math.sin( lat / 57.29578 )
    s = math.pow(s, 2) # s = sin(lat°) squared

	# 2.184e-6 is mean vertical gradient of gravity in m/s^2/decibar
    gravity_variation = 9.780318 * ( 1.0 + s * ( 5.2788e-3 + s * 2.36e-5 ) ) + 1.096e-6 * pres
    
    return specific_volume / gravity_variation # depth in meters



# This function takes a command string and sends individual bytes.
# command string
#   [0xff,0xff,0xff,0xff,0xaa,0x00,0x90,0x00,0x00,0x00,0x00,0x00,0x00,0x6c]
# It also reports the response.

def send_command(cmd_name, cmd_string):
    print ("\ncmd_name:", cmd_name)
    print ("cmd_string:", cmd_string)
    cmd_bytes = bytearray.fromhex(cmd_string)
    for cmd_byte in cmd_bytes:
        hex_byte = ("{0:02x}".format(cmd_byte))
        #print (hex_byte)
        ser.write(bytearray.fromhex(hex_byte))
        ser.write(serial.to_bytes([0xff,0xff,0xff,0xff,0xaa,0x00,0x90,0x00,0x00,0x00,0x00,0x00,0x00,0x6c]))
        time.sleep(.100)

    # wait an extra 3 seconds for DISP_ON_CMD
    if cmd_name == "DISP_ON_CMD":
        time.sleep(5.0)
    response = ser.read(32)
    print ("response:", binascii.hexlify(bytearray(response)))
    return

# This function takes a command string and sends individual bytes.
# command string
#   [0xff,0xff,0xff,0xff,0xaa,0x00,0x90,0x00,0x00,0x00,0x00,0x00,0x00,0x6c]
# It also reports the response.

def send_ctd(cmd_string):
    print ("cmd_string:", cmd_string)
    ser.write(serial.to_bytes([0xff,0xff,0xff,0xff,0xaa,0x00,0x90,0x00,0x00,0x00,0x00,0x00,0x00,0x6c]))
    
    response = ser.read(32)
    print ("response:", binascii.hexlify(bytearray(response)))
 
    read_ctd_values(response)
    return

# Event indicating client stop
stop_event = threading.Event()

def create_client():
    client = IoTHubModuleClient.create_from_edge_environment()

    # Define function for handling received messages
    async def receive_message_handler(message):
        # NOTE: This function only handles messages sent to "input1".
        # Messages sent to other inputs, or to the default, will be discarded
        if message.input_name == "input1":
            print("the data in the message received on input1 was ")
            print(message.data)
            print("custom properties are")
            print(message.custom_properties)
            print("forwarding mesage to output1")
            await client.send_message_to_output(message, "output1")

    try:
        # Set handler on the client
        client.on_message_received = receive_message_handler
    except:
        # Cleanup if failure occurs
        client.shutdown()
        raise

    return client


async def run_sample(client):
    # Customize this coroutine to do whatever tasks the module initiates
    # e.g. sending messages
    while True:
        send_ctd([0xff,0xff,0xff,0xff,0xaa,0x00,0x90,0x00,0x00,0x00,0x00,0x00,0x00,0x6c])
        await asyncio.sleep(1000)


def main():
    if not sys.version >= "3.5.3":
        raise Exception( "The sample requires python 3.5.3+. Current version of Python: %s" % sys.version )
    print ( "IoT Hub Client for Python" )

    # NOTE: Client is implicitly connected due to the handler being set on it
    client = create_client()

    # Define a handler to cleanup when module is is terminated by Edge
    def module_termination_handler(signal, frame):
        print ("IoTHubClient sample stopped by Edge")
        stop_event.set()

    # Set the Edge termination handler
    signal.signal(signal.SIGTERM, module_termination_handler)

    # Run the sample
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(run_sample(client))
    except Exception as e:
        print("Unexpected error %s " % e)
        raise
    finally:
        print("Shutting down IoT Hub Client...")
        loop.run_until_complete(client.shutdown())
        loop.close()


if __name__ == "__main__":
    main()
