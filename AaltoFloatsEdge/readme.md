# Floats IoT Edge Solution

Azure IoT Edge project for Floats.


## modules:

CTD, GNSS, DVL Altimeter sensor module to collect 
local log files (not to miss data in the case of )

## Getting started

1. Clone this repository
2. Open the folder in VS Code
3. Install Azure IoT Tools extension pack, Python 3.8 & other tools such as Docker

    https://docs.microsoft.com/en-us/azure/iot-edge/how-to-install-iot-edge?view=iotedge-2020-11

4. Start writing modules & debugging
5. Log in to azure registry for pushing images

az login (if needed)

`az login --scope https://management.core.windows.net//.default`

az acr login (needed basically once every time)

`az acr login --name aaltofloats`

```
sudo iotedge check
```

## log analytics

see Azuremonitoring readme.md

## iotedgedev
new thing - everything running in deocker container, not in host.
https://github.com/Azure/iot-edge-config


## azure iot sdk

https://github.com/Azure/azure-iot-sdk-python

## docker logs

docker logs size should be limited e.g. as logs might fill the memory.

in /etc/docker/daemon.json
```
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3" 
  }
}
```




## Netplan config


in /etc/netplan/*.yaml

```
# This file is generated from information provided by the datasource.  Changes
# to it will not persist across an instance reboot.  To disable cloud-init's
# network configuration capabilities, write a file
# /etc/cloud/cloud.cfg.d/99-disable-network-config.cfg with the following:
# network: {config: disabled}
network:
    ethernets:
        eth0:
            dhcp4: true
            optional: true
    version: 2
    wifis:
      wlan0:
        dhcp4: true
        optional: true
        access-points:
          "Zyxel_2581":
            password: "XXXXX"
```
## Ethernet with fixed IPv4 address

also in netplan config file:

## remote-ssh
in the case of issues, this might help


```
ssh-keygen -f "/home/jte/.ssh/known_hosts" -R "192.168.1.111"
```

## restart iotedge
```
sudo systemctl restart iotedge
```

iot edge 1.2

```
sudo iotedge check
```

start
``` 
sudo iotedge config apply
```

logs
```
iotedge logs <container name>
```

```
sudo aziotctl config apply
```

remove
```
sudo apt-get remove aziot-edge
```

## IOT HUB
requires a connection string for deploying new 

## Edge Modules

Azure IoT Edge projects consist of multiple different modules which communicate locally as well as with the remote IoT Hub via local "Edge Hub". The communication protocol between these modules is `MQTT` or `AMQP` (same as with the actual IoT Hub). Messaging is handled by the IoT Edge runtime, so all you have to do is to define the communication routes (sources and sinks) between modules and write message listeners and handlers for them.

The current Edge Hub routing config looks like this (see the deployment files):

```json
"$edgeHub": {
    "properties.desired": {
        "schemaVersion": "1.0",
        "routes": {
            "CANDataReaderToCANDataHandler": "FROM /messages/modules/CANDataReader/outputs/CANoutput INTO BrokeredEndpoint(\"/modules/CANDataHandler/inputs/input1\")",
            "CANData0ReaderToCANDataHandler": "FROM /messages/modules/CANData0Reader/outputs/CANoutput INTO BrokeredEndpoint(\"/modules/CANDataHandler/inputs/input1\")",
            "CANDataHandlerToIoTHub": "FROM /messages/modules/CANDataHandler/outputs/* INTO $upstream",
            "GPSReaderToIoTHub": "FROM /messages/modules/GPSReader/outputs/* INTO $upstream"
        },
        "storeAndForwardConfiguration": {
            "timeToLiveSecs": 7200
        }
    }
}
```

# DVL
- DVL
    direct TCP connection requires this connection

    ```
    sudo ip ad add 192.168.194.90/24 dev eth0
    ```
    
    can be done wit netplan config



# Blob storage

see: 
https://docs.microsoft.com/en-us/azure/iot-edge/how-to-deploy-blob?view=iotedge-2020-11
https://docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python?view=iotedge-2020-11&tabs=environment-variable-linux
https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-python-python-file-upload
https://github.com/Azure-Samples/azure-iotedge-blobstorage-sample/blob/master/modules/blobWriterModule/Program.cs


```	{
  "deviceAutoDeleteProperties": {
    "deleteOn": true,
    "deleteAfterMinutes": 1,
    "retainWhileUploading": true
  },
  "deviceToCloudUploadProperties": {
    "uploadOn": false,
    "uploadOrder": "OldestFirst",
    "cloudStorageConnectionString": "DefaultEndpointsProtocol=https;AccountName=aaltofloatstorage;AccountKey=Of6CmQ1twqk0Yoqul8NHg5iC5sR9FGnQLgDb35/yHl45tU8HM2k+3Fe3/ntgKxwc/7TzzskimqKgJJt1QR+7LA==; EndpointSuffix=core.windows.net",
    "storageContainersForUpload": {
      "$logs": {
        "target": "https://aaltofloatstorage.blob.core.windows.net/$logs"
      }
    },
    "deleteAfterUpload": true
  }
}```

### tricky thing in blob
volume mounting : created the needed folder for blob storage but access rights seems to be not enough for using the mounted folder.

in deployment json - 

"AzureBlobStorageonIoTEdge": {
            "settings": {
              "image": "mcr.microsoft.com/azure-blob-storage",
              "createOptions": "{\"HostConfig\":{\"Binds\":[\"/home/blob:/blobroot\"],\"PortBindings\":{\"11002/tcp\":[{\"HostPort\":\"11002\"}]}}}"
            },
            "type": "docker",
            "env": {
              "LOCAL_STORAGE_ACCOUNT_NAME": {
                "value": "$LOCAL_STORAGE_ACCOUNT_NAME"
              },
              "LOCAL_STORAGE_ACCOUNT_KEY": {
                "value": "$LOCAL_STORAGE_ACCOUNT_KEY"
              }
            },
            "status": "running",
            "restartPolicy": "always",
            "version": "1.0"
          }


# CAN

- CANData0Reader
  - reads CAN data from CAN bus 1 and sends the data to `CANDataHandler`
- CANDataReader
  - reads CAN data from CAN bus 2 and sends the data to `CANDataHandler`
- GPSReader
  - reads location every 1 minute and sends it to IoT Hub
- SimulatedCANData
  - Reads the CAN log `CSV` file from `SimulateCANData/test_data.csv` and sends the data to `CANDataHandler` like the `CANDataReader` would do in real environment. The data is sent in "real-time" according to the timestamps as it did occur when the data was originally captured.
- CANDataHandler
  - Processes the raw CAN data by decoding it according to the rules in `CANDataHandler/message_types.py` (see the file or guide below for decoding info). Sends the data to the IoT Hub.

## edge devices

### GPS


### CAN buses

canable [link](https://canable.io/)
typically visible in linux under can ports: ['/dev/ttyACM0', '/dev/ttyACM1']."


## How to decode CAN data

Most of the CAN bus data follows [SAE J1939](https://en.wikipedia.org/wiki/SAE_J1939) format.

The relevant fields in a CAN message are:

- Identifier, for example 18FEE900 (needs to be converted to decimal to get actual PGN value)
- 8 data bytes in HEX

The data bytes are decoded according to different rules depending on the message type (PGN). The message might contain multiple different values.

See the PGN values and decoding info from Floats documents. For example identifier 18FEE900 -> PGN 65257 (Fuel Consumption).

If we search the PGN from provided documents, we will find something like this:

> 2.6.25 Fuel Consumption (Liquid) (LFC)
>
> This message is transmitted, if parameter ZIZU_CANMESSAGE_FUEL_CONSUMPTION_TX_MASK is other than 'None'. The message is also transmitted to a bus where an active diagnostics session is detected.
>
> PGN 65257 (0xFEE9)
>
> Byte Parameter Resolution Offset SPN
>
> 1 – 4 Trip Fuel 0.5 l/bit 0 182
>
> 5 – 8 Total Fuel Used 0.5 l/bit 0 250

Example data bytes: 0 0 0 0 11 89 0 0

We are interested in the bytes 5 and 6 (the SPN number 250 is the J1939 parameter type and can be used when searching decoding information). To decode the bytes:

1. Select the relevant bytes from the PGN data field
    - 1189
2. Reverse the byte order if there is more than one byte (the data is in little endian format, MSB is the rightmost byte).
    - 9811
3. Convert the reversed hex to decimal
    - 38929
4. Apply the offset to the decimal
    - 38929 - 0 = 38929
5. Multiply the result with the resolution
    - 0.5 l / bit * 38929 = 19464.5 l
6. You have now the actual real value
    - 19464.5 l


#AZ
  if installed with 
  
  pip3 install azure-cli

  include PATH e.g. 
  export PATH="/home/pi/.local/bin:$PATH"