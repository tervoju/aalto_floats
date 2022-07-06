# direct method test

A technique that makes possible to send message/command to edge module.

1) for testing direct methods with IoT Hub and devices
2) generating "sensor" messages to iot hub based on status send with direct method 
    - sensor data forward to event hub
    - front end for sensor data

# example python module

with 
!) device twin
2) direct method
3) sensor data sending


# direct method links

https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-devguide-direct-methods

https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-mqtt-support#using-the-mqtt-protocol-directly


## authorization

```az iot hub generate-sas-token -n <iothubName> --du <duration>```

### example

```az iot hub generate-sas-token -n iothubvqc01 --du 48```

## example of the real time data 
https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-live-data-visualization-in-web-apps
https://github.com/Azure/azure-iot-sdk-python/blob/main/azure-iot-device/samples/pnp/simple_thermostat.py

# other links
https://docs.microsoft.com/en-us/azure/iot-develop/quickstart-send-telemetry-iot-hub?pivots=programming-language-python
 
 https://github.com/Azure/azure-iot-sdk-python/blob/main/azure-iot-device/samples/async-edge-scenarios/receive_data.py


## node & web app example

https://github.com/Azure-Samples/web-apps-node-iot-hub-data-visualization/tree/master/scripts

 "SharedAccessSignature sr=iothubvqc01.azure-devices.net&sig=AKkvaREHWjx73s0QLRHs3XBBkifTMTvVULiMbZ7RnI4%3D&se=1639739586&skn=iothubowner