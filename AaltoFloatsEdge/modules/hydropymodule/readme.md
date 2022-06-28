
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