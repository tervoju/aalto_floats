
## Getting started

1. Clone this repository
2. Open the folder in VS Code
3. Install Azure IoT Tools extension pack, Python 3.8 & other tools such as Docker
4. Start writing modules & debugging
5. Log in to azure registry for pushing images

needs this before pushing images

```
az acr login --name aaltofloats
```

# script

./module_status.sh aalto_floats_01 SimulatedDVL 10

# dvl modules

connected with ethernet cable. using address 192.168.194.95 to connect and port 16171

two types of messages 

### distances
{
  "time":76.33709716796875, milliseconds since last velocity report
  "vx":0.002135641174390912, 
  "vy":-0.00018836701929103583,
  "vz":-0.000037361100112320855,
  "fom":0.0009275538614019752, Figure of merit, a measure of the accuracy of the measured velocities (m/s)
  "altitude":0.09129234403371811, distance to bottom
  "transducers":[{"id":0,"velocity":-0.0006673489697277546,"distance":0.14160001277923584,"rssi":-25.822750091552734,"nsd":-97.3758773803711,"beam_valid":true},{"id":1,"velocity":-0.0005590454675257206,"distance":0.1534000039100647,"rssi":-26.124605178833008,"nsd":-96.05805206298828,"beam_valid":true},{"id":2,"velocity":0.0005750764976255596,"distance":0.08260000497102737,"rssi":-25.274274826049805,"nsd":-95.80996704101562,"beam_valid":true},{"id":3,"velocity":0.0005078003741800785,"distance":0.08260000497102737,"rssi":-26.258708953857422,"nsd":-97.38230895996094,"beam_valid":true}],
  "velocity_valid":true,
  "status":0,
  "format":"json_v2",
  "type":"velocity"
}

### dead reckoning
{
  "ts":1550139427.6284137, timestamp since last press of "reset button"
  "x":0.18743516047702605,
  "y":0.01702104496847002,
  "z":-0.05040616066696785,
  "std":0.4355372321949996,
  "roll":-0.9409523947358766, rotation around x axis
  "pitch":1.092898383237629, rotation around y axis
  "yaw":5.4970132268564225, rotation around z axis
  "type":"position_local",
  "status":0,
  "format":"json_v2"
}


# edge logs 
basics


set used account
```
az account set --subscription XXXX-Pay-As-You-Go
```


logging requires this add-on to az-cli add iot extension
```
az extension add --name azure-iot
```



check the extensions with
```

```


logs

az iot hub invoke-module-method --method-name 'GetModuleLogs' -n lannen-we-dev-iot-hub -d LT_IOT_E3_B56 -m '$edgeAgent' --method-payload \
'
    {
       "schemaVersion": "1.0",
       "items": [
          {
             "id": "edgeAgent",
             "filter": {
                "tail": 10
             }
          }
       ],
       "encoding": "none",
       "contentType": "text"
    }
'

## logs 

#### edgeAgent logs from the device

There some build-in direct remote methods for Azure IoT Edge 
[remote direct methods](https://docs.microsoft.com/en-us/azure/iot-edge/how-to-edgeagent-direct-method?view=iotedge-2020-11)

##### Methods

Ping
GetModuleLogs
RestartModule


```
az iot hub invoke-module-method --method-name 'GetModuleLogs' -n lannen-we-dev-iot-hub -d LT_IOT_E3_B56 -m '$edgeAgent' --method-payload '{ "schemaVersion": "1.0", "items": [{"id": "edgeAgent", "filter": {"tail": 10}}], "encoding": "none", "contentType": "text"}'
```

or

az iot hub invoke-module-method \
  -n lannen-we-dev-iot-hub \
  -d LT_IOT_E3_B56 \
  -m \$edgeAgent \
  --mn GetModuleLogs \
  --mp \
'
    {
        "schemaVersion": "1.0",
        "items": [
            {
                "id": "edge*",
                "filter": {
                    "tail": 10 
                }
            }
        ],
        "encoding": "none",
        "contentType": "json"
    }
' | jq '.payload[].payload | fromjson | .[].text' 


#### ping
```
az iot hub invoke-module-method --method-name 'ping' -n lannen-we-dev-iot-hub.azure-devices.net -d LT_IOT_E3_B56 -m '$edgeAgent'
```

az iot hub invoke-module-method \
  --method-name 'GetModuleLogs' \
  -n lannen-we-dev-iot-hub \
  -d LT_IOT_E3_B56 \
  -m '$edgeAgent' \
  --method-payload '{"contentType": "text","schemaVersion": "1.0","encoding": "gzip","items": [{"id": "edgeHub","filter": {"since": "2d","tail": 1000}}],}' \
  -o tsv --query 'payload[0].payloadBytes' \
  | base64 --decode \
  | gzip -d

#### module logs
```
  az iot hub invoke-module-method -n lannen-we-dev-iot-hub -d LT_IOT_E3_B56 -m \$edgeAgent --mn GetModuleLogs --mp '{"schemaVersion": "1.0","items": [{"id":"CANDataHandler","filter": {"tail": 10}}],"encoding": "none","contentType": "json"}' | jq '.payload[].payload | fromjson | .[].text' 
```
