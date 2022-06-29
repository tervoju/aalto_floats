
# trial for customer prometheus metrics

A short summary how to gather custom metrics from your IoT Edge modules in addition to the built-in metrics that the system modules provide. 
These are extension to the built-in metrics. However, system may require additional information from custom modules to create full status of the solution. 
Custom modules can be integrated into monitoring solution by using the appropriate Prometheus client library to emit metrics. 
This additional information can enable new views or alerts specialized system requirements.


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

