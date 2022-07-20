# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

import os
import asyncio
import sys
import signal
import threading
from azure.iot.device.aio import IoTHubModuleClient

import logging

# Event indicating client stop
stop_event = threading.Event()

#global settings for ADC samples
PAUSE = 0
TWIN_CALLBACKS = 0
NRO_ADC_OF_MEASUREMENTS = 2000000
LOG_PATH = '/app/logs/'

def get_ADC_samples(samples, pause):
    cmd = '/app/hydro/rawMCP3202 2000000 0'
    so = os.popen(cmd).read()
    print(so)

def remove_old_logs(type):
    global LOG_PATH
    log_files = LOG_PATH 
    logging.info("{}:{}".format("removing old logs", type))
    logging.info("{}:{}".format("log_files", log_files))
    try:
        filenames = [entry.name for entry in sorted(os.scandir(log_files),
            key=lambda x: x.stat().st_mtime, reverse=True)]
        # saves last two files
        for filename in filenames[2:]:
            filename_relPath = os.path.join(self.log_path, filename)
            if filename_relPath.__contains__(type):
                os.remove(filename_relPath)
    except Exception as ex:
        logging.info("{}:{}".format("Unexpected error in twin_patch_listener", ex ))


def create_client():
    client = IoTHubModuleClient.create_from_edge_environment()

    # Define function for handling received messages
    async def receive_message_handler(message):
        # NOTE: This function only handles messages sent to "input1".
        # Messages sent to other inputs, or to the default, will be discarded
        if message.input_name == "input1":
            logging.info('{}:{}'.format("message data", message.data))
            logging.info('{}:{}'.format("custom properties", message.custom_properties))
            await client.send_message_to_output(message, "output1")

     # DIRECT METHOD handling  
    # Define behavior for receiving direct messages 
    async def method_handler(method_request):
        global SENDING
        logging.info ("Direct Method handler - message")

        if method_request.name == "remove_adc_logs":
            logging.info("Received request for remove adc logs")
            remove_old_logs("adc")
            method_response = MethodResponse.create_from_method_request(
                method_request, 200, "removed old local ADC log files")
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
    async def receive_twin_patch_handler(twin_patch):
        global TWIN_CALLBACKS
        global NRO_ADC_OF_MEASUREMENTS
     
        try:
            logging.info( "The data in the desired properties patch was: %s" % twin_patch)
            if "telemetryConfig" in twin_patch:
                NRO_ADC_OF_MEASUREMENTS = int(twin_patch["telemetryConfig"]["nroOfMeasurements"])
                logging.info('{}:{}'.format("ADC measurements", NRO_ADC_OF_MEASUREMENTS ))
            TWIN_CALLBACKS += 1
            logging.info('{}:{}'.format("Total calls confirmed", TWIN_CALLBACKS ))
        except Exception as ex:
            logging.info('{}:{}'.format("Unexpected error in twin_patch_listener", ex ))

    try:
        # Set handler on the client
        client.on_message_received = receive_message_handler
        # Set handler for direct messages
        client.on_method_request_received = method_handler
        # Set handler for twin messages
        client.on_twin_desired_properties_patch_received = receive_twin_patch_handler
    except:
        # Cleanup if failure occurs
        client.shutdown()
        raise

    return client


async def run_hydro(client):
    global NRO_ADC_OF_MEASUREMENTS, PAUSE
    # Customize this coroutine to do whatever tasks the module initiates
    # e.g. sending messages
    while True:
        get_ADC_samples(NRO_ADC_OF_MEASUREMENTS, PAUSE)
        await asyncio.sleep(1000)


def main():
    if not sys.version >= "3.5.3":
        raise Exception( "The sample requires python 3.5.3+. Current version of Python: %s" % sys.version )
    logging.info ( "IoT Hub Client for Python - hydro native" )

    # NOTE: Client is implicitly connected due to the handler being set on it
    client = create_client()

    # Define a handler to cleanup when module is is terminated by Edge
    def module_termination_handler(signal, frame):
        logging.info ("IoTHubClient hydro native stopped by Edge")
        stop_event.set()

    # Set the Edge termination handler
    signal.signal(signal.SIGTERM, module_termination_handler)

    # Run the sample
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(run_hydro(client))
    except Exception as e:
        print("Unexpected error %s " % e)
        raise
    finally:
        logging.info("Shutting down IoT Hub Client ...")
        loop.run_until_complete(client.shutdown())
        loop.close()


if __name__ == "__main__":
    logging.basicConfig()
    logging.getLogger().setLevel(os.environ.get("LOGLEVEL", "INFO"))
    main()
