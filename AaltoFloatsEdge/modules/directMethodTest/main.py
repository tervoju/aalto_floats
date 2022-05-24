# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

# https://github.com/Azure/azure-iot-sdk-python/blob/main/azure-iot-device/samples/async-edge-scenarios/receive_data.py

import asyncio
import sys
import signal
import os
import threading
from azure.iot.device.aio import IoTHubModuleClient
from azure.iot.device import MethodResponse
from azure.iot.device import Message

import logging
import random
import json
from datetime import datetime
from datetime import timezone

#####################################################
# GLOBAL VARIABLES
SENDING = False
temperature = 60

# Event indicating client stop
stop_event = threading.Event()

#####################################################
# TELEMETRY TASKS - SEND data
async def send_telemetry_example(device_client, telemetry_msg):
    msg = Message(json.dumps(telemetry_msg))
    msg.content_encoding = "utf-8"
    msg.content_type = "application/json"
    await device_client.send_message_to_output(msg, "output1")
# END TELEMETRY TASKS
#####################################################

# define send message 
async def send_sensor_message(client):
    global MACHINE_SERIAL_NUMBER, temperature
    device_id = ""
    try:
        device_id = os.environ["IOTEDGE_DEVICEID"]
    except:
        device_id = 'silosimudev01'
    while True:
        delta = random.random() / 100
        current_temperature = temperature + delta
        temperature_msg1 = {"temperature": current_temperature, "humidity": current_temperature + 1}
        print(temperature_msg1)
        await send_telemetry_example(client, temperature_msg1)
        await asyncio.sleep(10)

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

    # DIRECT METHOD handling 
    # Define behavior for receiving methods 
    #
    async def method_handler(method_request):
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

    try:
        # Set handler on the client    
        client.on_message_received = receive_message_handler
        client.on_method_request_received = method_handler
    except:
        # Cleanup if failure occurs
        client.shutdown()
        raise

    return client


async def run_sample(client):
    # Customize this coroutine to do whatever tasks the module initiates
    # e.g. sending messages
    while True:
        await send_sensor_message(client)
        await asyncio.sleep(1)


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
    logging.basicConfig()
    logging.getLogger().setLevel(os.environ.get("LOGLEVEL", "INFO"))
    main()
