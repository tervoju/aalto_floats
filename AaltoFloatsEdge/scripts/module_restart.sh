if [ "$1" == "-h" ]; then
  echo "Usage: `basename $0`  "
  echo "  1 argument: device name "
  echo "  2 argument: module name to restart "
  exit 0
fi

echo 'device id:' $1
echo 'restart module: ' $2

az iot hub invoke-module-method \
-n lannen-we-dev-iot-hub \
-d $1 \
-m \$edgeAgent \
--mn RestartModule \
--mp '{"schemaVersion": "1.0", "id":"'$2'"}'
