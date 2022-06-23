# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

import asyncio
import sys
import os
import signal
import threading
from azure.iot.device.aio import IoTHubModuleClient

import logging
from gnss2csv import gnss2csv_file
import json


# Event indicating client stop
stop_event = threading.Event()
to_gnss_csv = gnss2csv_file()
gnss_row_limit = 30 # limit the size of the  gnss csv log, could be as module twin data 
gnss_row_cnt = 0
def create_client():
    client = IoTHubModuleClient.create_from_edge_environment()

    # Define function for handling received messages
    async def receive_message_handler(message):
        global to_gnss_csv, gnss_row_cnt, gnss_row_limit
        # NOTE: This function only handles messages sent to "input1".
        # Messages sent to other inputs, or to the default, will be discarded
        if message.input_name == "input1":
            #print("the data in the message received on input1 was ")
            #print(message.data)
            #print("custom properties are")
            #print(message.custom_properties)

            if message.custom_properties['type'] == "location":
                if gnss_row_cnt < gnss_row_limit:
                    print("storing message sensor values to logfile")
                    json_data = json.loads(message.data)
                    to_gnss_csv.write_csv_data(json_data) 
                    gnss_row_cnt = gnss_row_cnt + 1
                else:
                    gnss_row_cnt = 0
                    to_gnss_csv.close_csv_log()
                    to_gnss_csv = gnss2csv_file() # new file
            # not needed here
            # await client.send_message_to_output(message, "output1")

    try:
        # Set handler on the client
        client.on_message_received = receive_message_handler
    except:
        # Cleanup if failure occurs
        client.shutdown()
        raise
    return client

async def run_logmodule(client):
    # Customize this coroutine to do whatever tasks the module initiates
    # e.g. sending messages
    while True:
        # nothing here, waiting for messages
        await asyncio.sleep(1000)

def main():
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

    # Run the sample
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
