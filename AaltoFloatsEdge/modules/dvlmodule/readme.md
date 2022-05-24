# dvl message information

# ethernet connection

requires fixed ethernet address, can be set IPv4 to
`192.168.194.90`

`http://192.168.194.95`

sudo ip ad add 192.168.194.90/24 dev eth0
can be done in netplan as well

# axis

The axis on the DVL-A50 are oriented as follows:

    X axis is pointing forward (LED is forward, cable backward)
    Y axis is pointing right
    Z axis is pointing down (mounting holes are up, transducers are down)



## dvl message

{"time":81.95233154296875,
"vx":0.0010110485600307584,
"vy":-0.0007144125993363559,
"vz":-0.00028028266387991607,
"fom":0.0006783335120417178,
"altitude":0.09129234403371811,
"transducers":[
    {"id":0,"velocity":-0.0008826721459627151,"distance":0.14160001277923584,"rssi":-25.902250289916992,"nsd":-96.84258270263672,"beam_valid":true},
    {"id":1,"velocity":-0.00025184592232108116,"distance":0.1534000039100647,"rssi":-26.17237663269043,"nsd":-95.73751068115234,"beam_valid":true},
    {"id":2,"velocity":0.000026558060199022293,"distance":0.08260000497102737,"rssi":-25.71442413330078,"nsd":-95.33403778076172,"beam_valid":true},
    {"id":3,"velocity":0.00035340990871191025,"distance":0.08260000497102737,"rssi":-26.227529525756836,"nsd":-96.07746124267578,"beam_valid":true}
    ],
"velocity_valid":true,
"status":0,
"format":"json_v2",
"type":"velocity"
}

## imu message

{
    "ts":1550139418.777972, since last reset
"x":0.17759968728051115,
"y":0.015972922658754884,
"z":-0.0502442511532714,
"std":0.43320449363218216,
"roll":-0.9057042024049833,
"pitch":1.0713139028635779,
"yaw":5.27878490432063,
"type":"position_local",
"status":0,
"format":"json_v2"
}