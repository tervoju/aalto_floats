# direct method 

Direct Method is a technique that makes possible to send message/command to Edge module. IoT Hub hat the ability to invoke direct methods on devices from the cloud. Direct methods represent a request-reply interaction with a device similar to an HTTP call in that they succeed or fail immediately (after a user-specified timeout). This approach is useful for scenarios where the course of immediate action is different depending on whether the device was able to respond.  Direct method call is targeting single Edge device and module. 

Invoke a direct method through a service-facing URI ({iot hub}/twins/{device id}/methods/). A device receives direct methods through a device-specific MQTT topic ($iothub/methods/POST/{method name}/) 

Direct methods are useful in interactive scenarios where you want a device to act if and only if the device is online and receiving commands.  In these scenarios, you want to see an immediate success or failure so the cloud service can act on the result as soon as possible. The device may return some message body as a result of the method, but it isn't required for the method to do so. There is no guarantee on ordering or any concurrency semantics on method calls. Direct methods are synchronous and either succeed or fail after the timeout period (default: 30 seconds, settable between 5 and 300 seconds), there is no guaranteed response time, based on some simple and small scale test round trip time was ~300 ms.

The payload for method requests and responses is a JSON document up to 128 KB.

## Call URI

https://<iothubname>.azure-devices.net/twins/<deviceid>/modules/<moduleid/methods?api-version=2018-06-30

## authorization

```az iot hub generate-sas-token -n <iothubName> --du <duration>```

### example

```az iot hub generate-sas-token -n iothubvqc01 --du 48```



# direct method links

https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-devguide-direct-methods

https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-mqtt-support#using-the-mqtt-protocol-directly




## example of the real time data 
https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-live-data-visualization-in-web-apps
https://github.com/Azure/azure-iot-sdk-python/blob/main/azure-iot-device/samples/pnp/simple_thermostat.py

# other links
https://docs.microsoft.com/en-us/azure/iot-develop/quickstart-send-telemetry-iot-hub?pivots=programming-language-python
 
 https://github.com/Azure/azure-iot-sdk-python/blob/main/azure-iot-device/samples/async-edge-scenarios/receive_data.py


## node & web app example

https://github.com/Azure-Samples/web-apps-node-iot-hub-data-visualization/tree/master/scripts

 "SharedAccessSignature sr=iothubvqc01.azure-devices.net&sig=AKkvaREHWjx73s0QLRHs3XBBkifTMTvVULiMbZ7RnI4%3D&se=1639739586&skn=iothubowner