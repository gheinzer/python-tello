# tello
This simple Library should help you controlling the TELLO EDU over WiFi with Python

Tested on Windows 10.

## How to import
`from tello import tello
drone = tello([port=8890, ip="192.168.10.1"])`
### Port
Optional. Sets the port for controlling Tello and reading Data. Default is 8890.
### IP
Optional. The IP adress for controlling Tello and reading Data. Default is 192.168.10.1.

## Methods
### drone.takeoff()
Auto takeoff
### drone.land()
Auto landing.