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


### AOB

regex used for 

https://regex101.com/


