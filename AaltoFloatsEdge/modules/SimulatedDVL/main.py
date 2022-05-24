# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.

import time
import os
import sys
import asyncio
from six.moves import input
import threading
from azure.iot.device.aio import IoTHubModuleClient

from datetime import datetime
from datetime import timezone
import logging
import socket

TCP_IP = "192.168.194.95"
TCP_PORT = 16171

dataJson = ''

class TCPConnection:
    def __init__(self, sock=None, cliensocket=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def bind(self, host, port):
        while(1):
            try:
                self.sock.bind((host, port))
                logging.info('Successful Connection to simulate dvl')
                (clientsocket, address) = self.sock.accept()
                logging.info("connection found!")
                return 0
            except:
                logging.info('simulate dvl connection Failed')
                time.sleep(10)
                self.bind(host, port)
            
    def send_dvl(self, message):
        #CHECK CONNECTION
        r = message
        self.clientsocket.send(r.encode())        

#to bw checked
async def simulate_dvl_data(filename):
    """ Async generator function. Reads a sample file and replays the messages
        in real time as they occured during when the message file was captured.
    """
    line_count = 0
    sleep_time = 0
    cnt = 0
    with open(os.path.dirname(os.path.realpath(__file__)) + "/" + filename) as dvl_file:
        while True:
            line = dvl_file.readline()
            cnt += 1
            if not line:
                break
            print("Line {}: {}".format(cnt, line.strip()))
           
            await asyncio.sleep(0.5)
            yield line


async def main():
    try:
        if not sys.version >= "3.5.3":
            raise Exception( "The sample requires python 3.5.3+. Current version of Python: %s" % sys.version )
        print ( "IoT Hub Client for Python" )

        # The client object is used to interact with your Azure IoT hub.
        module_client = IoTHubModuleClient.create_from_edge_environment()

        # connect the client.
        await module_client.connect()

        # sends message to the iot edge hub, where the dvl data is decoded 
        # and determined if it needs to be send to cloud
        async def send_message(module_client, sender):
            async for message in simulate_dvl_data("org.txt"):
                print(message)
                sender.send_dvl(message)
                #await module_client.send_message_to_output(message, "DVLoutput")

        # define behavior for receiving an input message on input1
        async def input1_listener(module_client):
            while True:
                input_message = await module_client.receive_message_on_input("input1")  # blocking call
                print("the data in the message received on input1 was ")
                print(input_message.data)
                print("custom properties are")
                print(input_message.custom_properties)
                print("forwarding mesage to output1")
                await module_client.send_message_to_output(input_message, "output1")

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

        sender = TCPConnection()
        sender.bind(TCP_IP, TCP_PORT)

        # Schedule task
        sender = asyncio.gather(send_message(module_client, sender))

        # Run the stdin listener in the event loop
        loop = asyncio.get_event_loop()
        user_finished = loop.run_in_executor(None, stdin_listener)

        # Wait for user to indicate they are done listening for messages
        await user_finished

        # Cancel send
        sender.cancel()

        # Finally, disconnect
        await module_client.disconnect()

    except Exception as e:
        print ( "Unexpected error %s " % e )
        raise

if __name__ == "__main__":
    logging.basicConfig()
    logging.getLogger().setLevel(os.environ.get("LOGLEVEL", "INFO"))
    asyncio.run(main())