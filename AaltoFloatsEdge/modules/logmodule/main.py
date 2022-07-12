# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

import asyncio
import sys
import os
import signal
import threading
from azure.iot.device.aio import IoTHubModuleClient
from azure.iot.device import MethodResponse
from azure.iot.device import Message

import logging
from gnss2csv import gnss2csv_file
import json

# Event indicating client stop
stop_event = threading.Event()
to_gnss_csv = gnss2csv_file('/app/logs/')

gnss_row_limit = 30 # limit the size of the  gnss csv log, could be as module twin data 
gnss_row_cnt = 0

NRO_GNSS_OF_MEASUREMENTS = 1000
TWIN_CALLBACKS = 0

def create_client():
    client = IoTHubModuleClient.create_from_edge_environment()

    # MESSAGES handing
    async def receive_message_handler(message):
        global to_gnss_csv, gnss_row_cnt, gnss_row_limit, NRO_GNSS_OF_MEASUREMENTS
        # NOTE: This function only handles messages sent to "input1".
        # Messages sent to other inputs, or to the default, will be discarded
        if message.input_name == "input1":
            # logging.info('{}:{}'.format("message data", message.data))

            if message.custom_properties['type'] == "location":
                logging.info("storing message sensor values to logfile")
                if gnss_row_cnt >= NRO_GNSS_OF_MEASUREMENTS:
                    to_gnss_csv.close_csv_log()
                    to_gnss_csv = gnss2csv_file('/app/logs/') # new file
                    gnss_row_cnt = 0
                    
                json_data = json.loads(message.data)
                to_gnss_csv.write_csv_data(json_data) 
                gnss_row_cnt = gnss_row_cnt + 1
            # not needed here
            # await client.send_message_to_output(message, "output1")

    
    # DIRECT METHOD handling  
    # Define behavior for receiving direct messages 
    async def method_handler(method_request):
        global SENDING
        logging.info ("Direct Method handler - message")
        if method_request.name == "remove_all_logs":
            logging.info("Received request for removing all type logs")
            method_response = MethodResponse.create_from_method_request(
                method_request, 200, "remove data")
            await client.send_method_response(method_response)

        elif method_request.name == "remove_gnss_logs":
            logging.info("Received request for remove gnss logs")
            to_gnss_csv.remove_old_logs("gnss")
            method_response = MethodResponse.create_from_method_request(
                method_request, 200, "removed old local gnss log files")
            await client.send_method_response(method_response)

        elif (method_request.name == "start_send"):
            logging.info("Received request for start_send")
            SENDING = True
            method_response = MethodResponse.create_from_method_request(
                method_request, 200, "start_send"
            )
            await client.send_method_response(method_response)
        
        elif (method_request.name == "stop_send"):
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
        
    # TWIN PATCH handling
    # if the twin data is changed
    async def receive_twin_patch_handler(module_client):
        global TWIN_CALLBACKS
        global NRO_GNSS_OF_MEASUREMENTS
        while True:
            try:
                data = await module_client.receive_twin_desired_properties_patch()  # blocking call
                logging.info( "The data in the desired properties patch was: %s" % data)
                if data["telemetryConfig"]:
                    NRO_GNSS_OF_MEASUREMENTS = int(data["telemetryConfig"]["nroOfMeasurements"])
                TWIN_CALLBACKS += 1
                logging.info('{}:{}'.format("Total calls confirmed", TWIN_CALLBACKS ))
            except Exception as ex:
                print ( "Unexpected error in twin_patch_listener: %s" % ex )

    try:
        # Set handler for messages
        client.on_message_received = receive_message_handler
        # Set handler for direct messages
        client.on_method_request_received = method_handler
        # Set handler for d messages
        client.on_twin_desired_properties_patch_received = receive_twin_patch_handler

    except:
        # Cleanup if failure occurs
        client.shutdown()
        raise

    return client

async def run_logmodule(client):

    # check first the twin data 
    # "telemetryConfig": { "nroOfMeasurements": "100" },
    global NRO_GNSS_OF_MEASUREMENTS
    twin = await client.get_twin()
    if "telemetryConfig" in twin["desired"]:
        NRO_GNSS_OF_MEASUREMENTS = int(twin["desired"]["telemetryConfig"]["nroOfMeasurements"])
        logging.info('{}:{}'.format("NRO_GNSS_OF_MEASUREMENTS", NRO_GNSS_OF_MEASUREMENTS))
    else:
        logging.info("no telemetryConfig data")

    # Customize this coroutine to do whatever tasks the module initiates
    # e.g. sending messages
    while True:
        # nothing here, waiting for messages
        await asyncio.sleep(1000)

def main():
    global NRO_GNSS_OF_MEASUREMENTS
    if not sys.version >= "3.5.3":
        raise Exception( "The sample requires python 3.5.3+. Current version of Python: %s" % sys.version )
    print ( "IoT Hub Client for Python - logmodule" )

    # NOTE: Client is implicitly connected due to the handler being set on it
    client = create_client()

    # Define a handler to cleanup when module is is terminated by Edge
    def module_termination_handler(signal, frame):
        print ("IoTHubClient logmodule stopped by Edge")
        stop_event.set()

    # Set the Edge termination handler
    signal.signal(signal.SIGTERM, module_termination_handler)

    # Run the logmodule
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(run_logmodule(client))
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
