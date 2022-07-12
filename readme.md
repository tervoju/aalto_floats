# aalto floats edge


## iot edge development

assumption: 
1) develop modules with connected to iot hub
    set the
        1) properties -> module twin desired properties
        2) messages -> telemetry data
        3) commands -> direct method commands

2) when ready, can be connected to IoT Central with "ready" deployment json and module description, what messages, what commands

or

2) connect device to iot central (when sending data and it can create device model automatically)

## building the docker images

looks like there can be a tricky thing building docker images:
when developing linux /win environments, line endings. unvisible
characters in line ending can cause build to fail:

```
standard_init_linux.go:178: exec user process caused "exec format error"
The command '/bin/sh -c pip install -r requirements.txt' returned a non-zero code: 1
```


## IoT Central

https://docs.microsoft.com/en-us/azure/iot-central/core/concepts-device-authentication

generate rand with add that as key in iot central

```
openssl rand -base64 64
```

following values to config.toml (copy config edge template first as config.toml)

## DPS provisioning with symmetric key

```

[provisioning]
source = "dps"
global_endpoint = "https://global.azure-devices-provisioning.net"
id_scope = "0ne006376XX"

[provisioning.attestation]
method = "symmetric_key"
registration_id = "1lfrnfunxXX"
symmetric_key = { value = "xXem+5QsGxgqRx+BLMeTFUdZGbfRfg4cCu6a8i7q6QAfpwwH2Lp6zvFGYlFxDBU2bY/x0yS988Xm0B"}

# inline key (base64), or...
# symmetric_key = { uri = "file:///var/secrets/device-id.key" }                                          >
# symmetric_key = { uri = "pkcs11:slot-id=0;object=device%20id?pin-value=1234" }

```

after that start the iotedge again to take that in use.


in iot central create device template


### AOB

regex used for 

https://regex101.com/


