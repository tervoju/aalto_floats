# generated by VS Code IoT Tools extension IoT Edge module
# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

# 

import asyncio
import sys
import signal
import threading
from azure.iot.device.aio import IoTHubModuleClient
from azure.iot.device import MethodResponse
from azure.iot.device import Message

import os
import time
import serial
import sys
import binascii
import inspect
import codecs
import math
import pynmea2
import pyudev

import logging 

#global variables
atm_surface_pressure = 1.101325
lattitude = 59.8443631
#logging on
CTD_LOGGING_ON = 1
CTD_SENDING_FREQUENCY = 1
TWIN_CALLBACKS = 0

# usb / serial
USB_DEVICE_VENDOR = '0403'
USB_DEVICE_ID = '6011'

# this is the device id connected through usb - serial convertion box
# has to be connected to first plug
# Bus 001 Device 004: ID 0403:6011 Future Technology Devices International, Ltd FT4232H Quad HS USB-UART/FIFO IC
# ser = serial.Serial("/dev/ttyUSB1", baudrate=4800, timeout=0.5)
CTD_PORT = "/dev/ttyUSB1"
CTD_BAUDRATE = 4800
CTD_TIMEOUT = 0.5
global ctd_ser

def is_usb_serial(device, vid=None, pid=None):
    # Checks device to see if its a USB Serial device.
    # The caller already filters on the subsystem being 'tty'.
    # If serial_num or vendor is provided, then it will further check to
    # see if the serial number and vendor of the device also matches.

    #pprint.pprint(dict(device.properties))

    # cannot be right if no vendor id
    if 'ID_VENDOR' not in device.properties:
        return False
    # searcing for right vendor
    if vid is not None:
        if device.properties['ID_VENDOR_ID'] != vid:
            logging.info(vid + ' not found  ' + device.properties['ID_VENDOR_ID'])
            return False

    if pid is not None:
        if device.properties['ID_MODEL_ID'] != pid:
            logging.info('not found')
            return False
    return True

def list_devices(vid=None, pid=None):
    devs = []
    context = pyudev.Context()
    for device in context.list_devices(subsystem='tty'):
        if is_usb_serial(device, vid= vid,  pid = pid):
            devs.append(device.device_node)
    return devs

# $  A  Q  C  T  D  
# in hex:
#  24 41 51 43 54 44 2c 32 33 2e 32 34 382c30312e3031302c30302e3030342a37410d0a
# example of CTD message
# b'$AQCTD,23.268,01.012,-00.000*53\r'

## intepredign string from CTD
def read_ctd_values(ctd_response):
  
    # check if there is no response from CTD
    if len(ctd_response) == 0:
        return -1,0,0,0
    # check the response for relevance
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
    global ctd_ser
    print ("\ncmd_name:", cmd_name)
    print ("cmd_string:", cmd_string)
    cmd_bytes = bytearray.fromhex(cmd_string)
    for cmd_byte in cmd_bytes:
        hex_byte = ("{0:02x}".format(cmd_byte))
        #print (hex_byte)
        ctd_ser.write(bytearray.fromhex(hex_byte))
        ctd_ser.write(serial.to_bytes([0xff,0xff,0xff,0xff,0xaa,0x00,0x90,0x00,0x00,0x00,0x00,0x00,0x00,0x6c]))
        time.sleep(.100)

    # wait an extra 3 seconds for DISP_ON_CMD
    if cmd_name == "DISP_ON_CMD":
        time.sleep(5.0)
    response = ctd_ser.read(32)
    print ("response:", binascii.hexlify(bytearray(response)))
    return

# This function takes a command string and sends individual bytes.
# command string
#   [0xff,0xff,0xff,0xff,0xaa,0x00,0x90,0x00,0x00,0x00,0x00,0x00,0x00,0x6c]
# It also reports the response.

def send_ctd(cmd_string):
    global ctd_ser
    print ("cmd_string:", cmd_string)
    ctd_ser.write(serial.to_bytes([0xff,0xff,0xff,0xff,0xaa,0x00,0x90,0x00,0x00,0x00,0x00,0x00,0x00,0x6c]))
    
    response = ctd_ser.read(32)
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
            logging.info("{}:{}".format("the data in the message received on input1 was ", message.data))
            logging.info("{}:{}".format("custom properties are", message.custom_properties))
            logging.info("forwarding mesage to output1")
            await client.send_message_to_output(message, "output1")
    
        # DIRECT METHOD handling  
    # Define behavior for receiving direct messages 
    async def direct_method_handler(method_request):
        global SENDING
        logging.info ("Direct Method handler - message")
        if method_request.name == "get_data":
            logging.info("Received request for get_data")
            method_response = MethodResponse.create_from_method_request(
                method_request, 200, "some data"
            )
            await client.send_method_response(method_response)

        if (method_request.name == "start_send"):
            logging.info("Received request for start_send")
            SENDING = True
            method_response = MethodResponse.create_from_method_request(
                method_request, 200, "start_send"
            )
            await client.send_method_response(method_response)
        
        if (method_request.name == "stop_send"):
            logging.info("Received request for stop_send")
            SENDING = False
            method_response = MethodResponse.create_from_method_request(
                method_request, 200, "stop_send"
            )
            await client.send_method_response(method_response)

        else:
            print("Unknown method request received: {}".format(method_request.name))
            method_response = MethodResponse.create_from_method_request(method_request, 400, None)
            await client.send_method_response(method_response)
    
    # currently only sendFrequency value handled
    async def receive_twin_patch_handler(module_client):
        global TWIN_CALLBACKS
        global CTD_SENDING_FREQUENCY
        while True:
            try:
                data = await module_client.receive_twin_desired_properties_patch()  # blocking call
                logging.info( "The data in the desired properties patch was: %s" % data)
                if data["desired"]["telemetryConfig"]:
                    CTD_SENDING_FREQUENCY = int(data["desired"]["telemetryConfig"]["sendFrequency"])*60
                TWIN_CALLBACKS += 1
                logging.info ("{}:{}".format("Total calls confirmed: ", TWIN_CALLBACKS ))
            except Exception as ex:
                logging.info("{}:{}".format("Unexpected error in twin_patch_listener: ", ex ))

    try:
        # Set handler for messages
        client.on_message_received = receive_message_handler
        # Set handler for direct messages
        client.on_method_request_received = direct_method_handler
        # Set handler for d messages
        client.on_twin_desired_properties_patch_received = receive_twin_patch_handler
    except:
        # Cleanup if failure occurs
        client.shutdown()
        raise

    return client


async def run_ctd(client):
   
    # Customize this coroutine to do whatever tasks the module initiates
    # e.g. sending messages
    while True:
        send_ctd([0xff,0xff,0xff,0xff,0xaa,0x00,0x90,0x00,0x00,0x00,0x00,0x00,0x00,0x6c])
        # this should also send the message of the measurement as depth
        # possibly make log measurements of the message
        # 
        await asyncio.sleep(1000)


# 1) create connection
# 2) read device twin data
# 3) direct message handling : logging or not , frequency
# 4) start record CTD measurements

def main():
    global ctd_ser
    if not sys.version >= "3.5.3":
        raise Exception( "The sample requires python 3.5.3+. Current version of Python: %s" % sys.version )
    logging.info( "IoT Hub Client for CTD - Python" )

    # NOTE: Client is implicitly connected due to the handler being set on it
    client = create_client()

    # define port for GPS USB module
    ctd_port = CTD_PORT
    CTD_PORTS = list_devices(USB_DEVICE_VENDOR, USB_DEVICE_ID)
    print(CTD_PORTS)
    if CTD_PORTS != []:
        print('USB CTD DEVICE FOUND')
        ctd_port = CTD_PORTS[0] # select first for device
    else:
        print('NO RIGHT CTD DEVICE FOUND')

    # GPS receiver
    ctd_ser = serial.Serial(ctd_port, baudrate=CTD_BAUDRATE, timeout=CTD_TIMEOUT)
    
    # Define a handler to cleanup when module is is terminated by Edge
    def module_termination_handler(signal, frame):
        print ("IoTHubClient sample stopped by Edge")
        stop_event.set()

    # Set the Edge termination handler
    signal.signal(signal.SIGTERM, module_termination_handler)

    # Run the sample
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(run_ctd(client))
    except Exception as e:
        print("Unexpected error %s " % e)
        raise
    finally:
        print("Shutting down IoT Hub Client...")
        loop.run_until_complete(client.shutdown())
        loop.close()


if __name__ == "__main__":
    logging.basicConfig()
    logging.getLogger().setLevel(os.environ.get("LOGLEVEL", "INFO"))
    main()
