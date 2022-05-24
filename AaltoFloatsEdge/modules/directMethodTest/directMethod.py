import requests
import json

# example of sending direct method with python script to device module
# Authorization needs to be updated 

url = "https://iothubvqc01.azure-devices.net/twins/silosimudev01/modules/directMethodTest/methods?api-version=2018-06-30"

payload = json.dumps({
  "methodName": "get_data",
  "responseTimeoutInSeconds": 5,
  "payload": {
    "test": "test"
  }
})
headers = {
  'Authorization': 'SharedAccessSignature sr=iothubvqc01.azure-devices.net&sig=U7j3jR6Bf5qmELQSmlX8EbvrsHRRlg9wcSoRw3BK03E%3D&se=1640932404&skn=iothubowner',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
