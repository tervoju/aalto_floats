# edge features

example for azure edge digital twin data and direct methods

# message handling

# direct method

# digital twins

Device/module twins are JSON documents that store device state information, including metadata, configurations, and conditions. IoT Hub persists a device twin for each device that connects to it.

Device/module twin data/settings is visible in Azure portal or in also in deployment json.

Each module has 'Module Identity Twin' for twin settings as 'Tag', 'desired' and 'reported' twim data. 

Note: device twin data has not been visible in modules, assuming this the case still.  


below code to get digital twin data 


when starting module check module twin
```
    # check first the twin data 
    # "telemetryConfig": { "nroOfMeasurements": "100" },
    global NRO_GNSS_OF_MEASUREMENTS
    twin = await client.get_twin()
    if "telemetryConfig" in twin["desired"]:
        NRO_GNSS_OF_MEASUREMENTS = int(twin["desired"]["telemetryConfig"]["nroOfMeasurements"])
        logging.info(NRO_GNSS_OF_MEASUREMENTS)
    else:
        logging.info("no telemetryConfig data")
```


```
    async def receive_twin_patch_handler(module_client):
        global TWIN_CALLBACKS
        global NRO_GNSS_OF_MEASUREMENTS
        while True:
            try:
                data = await module_client.receive_twin_desired_properties_patch()  # blocking call
                logging.info( "The data in the desired properties patch was: %s" % data)
                if data["desired"]["telemetryConfig"]:
                    NRO_GNSS_OF_MEASUREMENTS = int(data["desired"]["telemetryConfig"]["nroOfMeasurements"])*60
                TWIN_CALLBACKS += 1
                print ( "Total calls confirmed: %d\n" % TWIN_CALLBACKS )
            except Exception as ex:
                print ( "Unexpected error in twin_patch_listener: %s" % ex )
```


see some info from here

https://docs.microsoft.com/en-us/azure/iot-edge/tutorial-python-module?view=iotedge-2020-11&WT.mc_id=IoT-MVP-5002324

https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-python-twin-getstarted

https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-devguide-device-twins


