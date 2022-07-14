# Monitoring solution 



## Azure log analytics

some quides with generic description how monitoring can be taken into use.

https://docs.microsoft.com/en-us/azure/iot-edge/how-to-collect-and-transport-metrics?view=iotedge-2020-11&tabs=iothub

https://docs.microsoft.com/en-us/azure/iot-edge/tutorial-monitor-with-workbooks?view=iotedge-2020-11


### Cloud
Azure cloud services used:
- Iot Hub
- Log Analytics workspace



### Edge
Requires monitoring module `azureiotedge-metrics-collector` and settings in deployment for Azure edgeAgent module `mcr.microsoft.com/azureiotedge-agent`. See below: 

```
 "edgeAgent": {
            "type": "docker",
            "settings": {
              "image": "mcr.microsoft.com/azureiotedge-agent:1.2",
              "createOptions": {}
            },
            "env": {
              "ResourceId": {
                "value": "$AZURE_IOTHUB_RESOURCE_ID"
              },
              "UploadTarget": {
                "value": "$AZURE_UPLOAD_TARGET"
              },
              "LogAnalyticsWorkspaceId": {
                "value": "$AZURE_WORKSPACE_ID"
              },
              "LogAnalyticsSharedKey": {
                "value": "$AZURE_PRIMARY_KEY"
              }
            }
          },
```

and following setting for metrics collector module.


```
  "IoTEdgeMetricsCollector": {
            "settings": {
              "image": "mcr.microsoft.com/azureiotedge-metrics-collector:1.0",
              "createOptions": ""
            },
            "type": "docker",
            "env": {
              "ResourceId": {
                "value": "$AZURE_IOTHUB_RESOURCE_ID"
              },
              "UploadTarget": {
                "value": "$AZURE_UPLOAD_TARGET"
              },
              "LogAnalyticsWorkspaceId": {
                "value": "$AZURE_WORKSPACE_ID"
              },
              "LogAnalyticsSharedKey": {
                "value": "$AZURE_PRIMARY_KEY"
              },
              "MetricsEndpointsCSV": {
                "value": "http://edgeAgent:9600/metrics,http://edgeHub:9600/metrics,http://hydropymodule:9600/metrics"
              }
            },
            "status": "running",
            "restartPolicy": "always",
            "version": "1.0"
          },
```


### custom metrics

https://docs.microsoft.com/en-us/azure/iot-edge/how-to-add-custom-metrics?view=iotedge-2020-11


Following setting for metrics collector module. what is noteworthy is the format for custom metrics from certain module

```
  "MetricsEndpointsCSV": {
                "value": "http://edgeAgent:9600/metrics,http://edgeHub:9600/metrics,http://hydropymodule:9600/metrics"
   }
```

any module that needs to be checked for custom metrics needs to be added as endpoint to the string list (has to be in this
format)

#### python version to add custom modules



## local monitoring

it is possible to see metrics locally with grafana and prometheus

using grafana in docker 

https://ducko.uk/installing-grafana-prometheus-via-docker-to-monitor-raspberry-pi-metrics/


```
 docker run -d -p 3000:3000 grafana/grafana-oss
```

expose edgehub and edgeagent ports

e.g. edgeHub to 9602

```
"ExposedPorts": {
    "9600/tcp": {}
},
"HostConfig": {
    "PortBindings": {
        "5671/tcp": [
            {
                "HostPort": "5671"
            }
        ],
        "8883/tcp": [
            {
                "HostPort": "8883"
            }
        ],
        "443/tcp": [
            {
                "HostPort": "443"
            }
        ],
        "9600/tcp": [
            {
                "HostPort": "9602"
            }
        ]
    }
}
```
and after deplyment you can see e.g. in the same network

http://192.168.8.104:9602/metrics

```
# HELP edgehub_messages_sent_total Messages sent from edge hub
# TYPE edgehub_messages_sent_total counter
# HELP edgehub_message_send_duration_seconds Time taken to send a message
# TYPE edgehub_message_send_duration_seconds summary
# HELP edgehub_queue_length Number of messages pending to be processed for the endpoint
# TYPE edgehub_queue_length gauge
edgehub_queue_length{iothub="iothubvqc01.azure-devices.net",edge_device="rasp4-trial",instance_number="b0e77009-b239-4cc6-b04f-4825a75a032d",endpoint="iothub",priority="2000000000",ms_telemetry="True"} 0
edgehub_queue_length{iothub="iothubvqc01.azure-devices.net",edge_device="rasp4-trial",instance_number="b0e77009-b239-4cc6-b04f-4825a75a032d",endpoint="rasp4-trial/logmodule/input1",priority="2000000000",ms_telemetry="True"} 0
# HELP edgehub_reported_properties_update_duration_seconds Time taken to update reported properties
# TYPE edgehub_reported_properties_update_duration_seconds summary
edgehub_reported_properties_update_duration_seconds_sum{iothub="iothubvqc01.azure-devices.net",edge_device="rasp4-trial",instance_number="b0e77009-b239-4cc6-b04f-4825a75a032d",target="upstream",id="rasp4-trial/$edgeHub"} 0.7779749
edgehub_reported_properties_update_duration_seconds_count{iothub="iothubvqc01.azure-devices.net",edge_device="rasp4-trial",instance_number="b0e77009-b239-4cc6-b04f-4825a75a032d",target="upstream",id="rasp4-trial/$edgeHub"} 1
edgehub_reported_properties_update_duration_seconds{iothub="iothubvqc01.azure-devices.net",edge_device="rasp4-trial",instance_number="b0e77009-b239-4cc6-b04f-4825a75a032d",target="upstream",id="rasp4-trial/$edgeHub",quantile="0.1"} 0.7779749
edgehub_reported_properties_update_duration_seconds{iothub="iothubvqc01.azure-devices.net",edge_device="rasp4-trial",instance_number="b0e77009-b239-4cc6-b04f-4825a75a032d",target="upstream",id="rasp4-trial/$edgeHub",quantile="0.5"} 0.7779749
edgehub_reported_properties_update_duration_seconds{iothub="iothubvqc01.azure-devices.net",edge_device="rasp4-trial",instance_number="b0e77009-b239-4cc6-b04f-4825a75a032d",target="upstream",id="rasp4-trial/$edgeHub",quantile="0.9"} 0.7779749
edgehub_reported_properties_update_duration_seconds{iothub="iothubvqc01.azure-devices.net",edge_device="rasp4-trial",instance_number="b0e77009-b239-4cc6-b04f-4825a75a032d",target="upstream",id="rasp4-trial/$edgeHub",quantile="0.99"} 0.7779749
```

### prometheus installation & configuration

https://www.petecodes.co.uk/configuring-and-visualising-iot-edge-metrics-using-prometheus-and-grafana/
