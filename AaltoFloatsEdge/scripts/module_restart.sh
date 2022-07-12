if [ "$1" == "-h" ]; then
  echo "Usage: `basename $0`  "
  echo "  1 argument: hub name "
  echo "  2 argument: device name "
  echo "  3 argument: module name to restart "
  exit 0
fi

echo 'hub :' $1
echo 'device id:' $2
echo 'restart module: ' $3

az iot hub invoke-module-method \
-n iothubvqc01.azure-devices \
-d $2 \
-m \$edgeAgent \
--mn RestartModule \
--mp '{"schemaVersion": "1.0", "id":"'$3'"}'