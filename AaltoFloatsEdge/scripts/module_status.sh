#!/bin/bash
if [ "$1" == "-h" ]; then
  echo "Usage: `basename $0`  "
  echo "  1 argument: device name  "
  echo "  2 argument: module name  "
  echo "  3 argument: number of logging lines  "
  exit 0
fi

echo 'device id:' $1
echo 'getting module logs: ' $2
echo 'last ' $3 ' log lines'

az iot hub invoke-module-method \
-n iot-floats \
-d $1 \
-m \$edgeAgent \
--mn GetModuleLogs \
--mp '{"schemaVersion": "1.0","items": [{"id":"'$2'","filter": {"tail": '$3'}}],"encoding": "none","contentType": "json"}' | jq '.payload[].payload | fromjson | .[].text'
