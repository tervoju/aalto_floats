import requests
import json
import time
from datetime import datetime


print("starting direct method call")

url = "https://iothubvqc01.azure-devices.net/twins/silosimudev01/modules/directMethodTest/methods?api-version=2018-06-30"

payload = json.dumps({
  "methodName": "get_data",
  "responseTimeoutInSeconds": 5,
  "payload": {
    "test": "test"
  }
})
headers = {
  'Content-Type': 'application/json',
  'Authorization': 'SharedAccessSignature sr=iothubvqc01.azure-devices.net&sig=1qh%2FG8uBMDvdQlxlOcAROaGsYmiQIJZtRM2ngdFnXbU%3D&skn=iothubowner&se=1640094726',
  'Accept': '*/*'
}


for x in range(100):
    timestr = time.strftime("%Y%m%d-%H%M%S")
    start_time = datetime.now().timestamp()
    response = requests.request("POST", url, headers=headers, data=payload)
    end_time = datetime.now().timestamp()
    print(response.text + ", " + str(end_time - start_time))
    time.sleep(1)