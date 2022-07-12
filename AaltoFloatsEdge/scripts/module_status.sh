#!/bin/bash
if [ "$1" == "-h" ]; then
  echo "Usage: `basename $0`  "
  echo "  1 argument: hub name"
  echo "  2 argument: device name  "
  echo "  3 argument: module name  "
  echo "  4 argument: number of logging lines  "
  exit 0
fi

echo 'hub: ' $1
echo 'device id:' $2
echo 'getting module logs: ' $3
echo 'last ' $4 ' log lines'

az iot hub invoke-module-method \
-n $1 \
-d $2 \
-m \$edgeAgent \
--mn GetModuleLogs \
--mp '{"schemaVersion": "1.0","items": [{"id":"'$3'","filter": {"tail": '$4'}}],"encoding": "none","contentType": "json"}' | jq '.payload[].payload | fromjson | .[].text'
