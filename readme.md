# aalto floats edge


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


