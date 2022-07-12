
# scripts

example:

./module_status.sh aalto_floats_01 SimulatedDVL 10


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
