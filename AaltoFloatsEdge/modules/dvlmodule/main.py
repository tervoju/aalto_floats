import socket
import time
import sys
import os
import logging
import json
import csv

from flatten_json import flatten
from datetime import datetime
from datetime import timezone

from six.moves import input
from azure.iot.device.aio import IoTHubModuleClient
from azure.iot.device import MethodResponse
from azure.iot.device import Message

import threading
import asyncio
from functools import wraps, partial

from dvl_socket import TCPConnection

# for socket to DVL A50
TCP_IP = "192.168.194.95"
TCP_PORT = 16171
deviceid = "SUB"

#logging on
DVL_LOGGING_ON = 1
DVL_SENDING_FREQUENCY = 1
TWIN_CALLBACKS = 0

#
#   
async def main():
    global TCP_IP, TCP_PORT, csv_file_time, csv_writer_time, csv_file_ts, csv_writer_ts

    try:
        if not sys.version >= "3.5.3":
            raise Exception( "The sample requires python 3.5.3+. Current version of Python: %s" % sys.version )
        logging.info("IoT Hub Client for Python: dvlmodule")

        # The client object is used to interact with your Azure IoT hub.
        module_client = IoTHubModuleClient.create_from_edge_environment()

        # connect the client.
        await module_client.connect()

        twin = await module_client.get_twin()
        # "telemetryConfig": { "sendFrequency": "10" },
        # in minutes
        if "telemetryConfig" in twin["desired"]:
            telemetry = twin["desired"]["telemetryConfig"]
            DVL_SENDING_FREQUENCY = int(telemetry["sendFrequency"])
            logging.info(DVL_SENDING_FREQUENCY)
        else:
            logging.info(twin)
            logging.info("no telemetryConfig data")

        
        # define behavior for receiving an input message on input1
        async def input1_listener(module_client):
            while True:
                input_message = await module_client.on_message_received("input1")  # blocking call
                print("the data in the message received on input1 was ")
                print(input_message.data)
                print("custom properties are")
                print(input_message.custom_properties)
                print("forwarding mesage to output1")
                await module_client.send_message_to_output(input_message, "output1")

        # currently only sendFrequency value handled
        async def twin_patch_listener(module_client):
            global TWIN_CALLBACKS
            global DVL_SENDING_FREQUENCY
            while True:
                try:
                    data = await module_client.receive_twin_desired_properties_patch()  # blocking call
                    logging.info( "The data in the desired properties patch was: %s" % data)
                    if data["desired"]["telemetryConfig"]:
                         DVL_SENDING_FREQUENCY = int(data["desired"]["telemetryConfig"]["sendFrequency"])
                    TWIN_CALLBACKS += 1
                    logging.info ("{}:{}".format("Total calls confirmed: ", TWIN_CALLBACKS ))
                except Exception as ex:
                   logging.info("{}:{}".format("Unexpected error in twin_patch_listener: ", ex ))
        
        # define behavior for halting the application
        def stdin_listener():
            while True:
                try:
                    selection = input("Press Q to quit\n")
                    if selection == "Q" or selection == "q":
                        print("Quitting...")
                        break
                except:
                    time.sleep(10)
        
        listen = TCPConnection(module_client)
        await listen.connect(TCP_IP, TCP_PORT)
        logging.info( "The dvl module TCP socket is connected ")
            
        # Schedule task for C2D Listener
        listeners = asyncio.gather(listen.read_dvl())
        logging.info( "The dvlmodule is now waiting for messages from DVL A50. ")

        # Run the stdin listener in the event loop
        loop = asyncio.get_event_loop()
        user_finished = loop.run_in_executor(None, stdin_listener)

        # Wait for user to indicate they are done listening for messages
        await user_finished

        # Cancel listening
        listeners.cancel()

        # Finally, disconnect
        await module_client.disconnect()

    except Exception as e:
        print ( "Unexpected error %s " % e )
        raise

if __name__ == '__main__' : 
    logging.basicConfig()
    logging.getLogger().setLevel(os.environ.get("LOGLEVEL", "INFO"))
    asyncio.run(main())
  
