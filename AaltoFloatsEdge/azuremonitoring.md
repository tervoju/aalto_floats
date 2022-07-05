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



###
