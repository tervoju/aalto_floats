
# Azure monitor integration

https://docs.microsoft.com/en-us/azure/iot-edge/how-to-collect-and-transport-metrics?view=iotedge-2020-11&tabs=iothub


# trial for custom prometheus metrics

A short summary how to gather custom metrics from your IoT Edge modules in addition to the built-in metrics that the system modules provide. 
These are extension to the built-in metrics. However, system may require additional information from custom modules to create full status of the solution. 
Custom modules can be integrated into monitoring solution by using the appropriate Prometheus client library to emit metrics. 
This additional information can enable new views or alerts specialized system requirements.

# example deployment.json
https://github.com/Azure/iotedge/blob/release/1.1/edge-modules/metrics-collector/src/ExampleDeployment.json


## Azure monitoring settings
AZURE_IOTHUB_RESOURCE_ID=/subscriptions/XXXb1ae8-2b59-4496-8630-29a121b81700/resourceGroups/silo_XXX/providers/Microsoft.Devices/IotHubs/iothubXXXX
AZURE_UPLOAD_TARGET=AzureMonitor
AZURE_WORKSPACE_ID=XXXe92af-fca6-4e30-90b6-e9aef950b1bd
AZURE_PRIMARY_KEY=XXXSIqF/HSFTA0lT891x/hpz3rUvSFjOrwAw52YD5dyhI53gAR7eR3ynYunKmhccn0eFflqWgWKasKKyAU+9Og==

## EXAMPLE

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

[Short intro to custom metrics](https://docs.microsoft.com/en-us/azure/iot-edge/how-to-add-custom-metrics?view=iotedge-2020-11)


requires additional prometheus client library

https://prometheus.io/docs/instrumenting/clientlibs/


and specially for python code:

[python client library](https://github.com/prometheus/client_python)

```
pip install prometheus_client
```

c# example of the custom 
https://github.com/Azure-Samples/iotedge-module-prom-custom-metrics/blob/b6b8501adb484521b76e6f317fefee57128834a6/csharp/Program.cs#L49


## test

check if the custom metrics is available with command

```
sudo docker exec replace-with-metrics-collector-module-name curl http://replace-with-custom-module-name:9600/metrics
```
e.g.

```
sudo docker exec IoTEdgeMetricsCollector curl http://hydropymodule:9600/metrics
```

## azure logs

check that logs are received in Azure in IoT Hub / Monitoring / Logs part by adding query

```
InsightsMetrics
| where Name == 'replace-with-custom-metric-name'
```


## workbook

### Customize workbooks
Azure Monitor workbooks are customizable. You can edit the public templates to suit your requirements. All the visualizations are driven by resource-centric `Kusto Query Language` queries on the InsightsMetrics table.

To begin customizing a workbook, first enter editing mode. Select the Edit button in the menu bar of the workbook. Curated workbooks make extensive use of workbook groups. You may need to select Edit on several nested groups before being able to view a visualization query.

