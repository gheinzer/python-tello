# tello
This simple Library should help you controlling the TELLO EDU over WiFi with Python

Tested on Windows 10.

## Installation
You can install this Library via PIP:
```python
pip install tello
```
If you don't want to install the library via PIP, you can move the `tello.py` file to your working directory.

## How to import
### When you moved the library to your working directory (not installed with PIP)
```python
from tello import tello
drone = tello([port=8890, ip="192.168.10.1"])
```
#### Port
Optional. Sets the port for controlling Tello and reading Data. Default is 8890.
#### IP
Optional. The IP adress for controlling Tello and reading Data. Default is 192.168.10.1.

### When you installed the library via PIP
```python
import tello
drone = tello.tello([port=8890, ip="192.168.10.1"])
#### Port
Optional. Sets the port for controlling Tello and reading Data. Default is 8890.
#### IP
Optional. The IP adress for controlling Tello and reading Data. Default is 192.168.10.1.

## Methods
### Send a Command to the Drone
```python
drone.cmd(command)
```
You can send a command like `up 99` to the drone with `drone.cmd()`
#### Command
Required. The Command to send to the drone.
### Takeoff
```python
drone.takeoff()
```
Auto takeoff
### Land
```python
drone.land()
```
Auto landing.
### Set Speed
```python
drone.setSpeed(speed)
```
Set the speed of the drone in cm/s.
#### Speed
Required. The Speed to set. Has to be between 10 and 100.
### Fly up
```python
drone.up(distance)
```
#### Distance
Required. The distance to ascend in cm. Has to be between 20 and 500.
### Fly down
```python
drone.down(distance)
```
#### Distance
Required. The distance to descend in cm. Has to be between 20 and 500.
### Fly forward
```python
drone.forward(distance)
```
#### Distance
Required. The distance to fly forward in cm. Has to be between 20 and 500.
### Fly backward
```python
drone.backward(distance)
```
#### Distance
Required. The distance to fly backward in cm. Has to be between 20 and 500.
### Fly right
```python
drone.right(distance)
```
#### Distance
Required. The distance to fly right in cm. Has to be between 20 and 500.
### Fly left
```python
drone.left(distance)
```
#### Distance
Required. The distance to fly left in cm. Has to be between 20 and 500.
### Make a Flip
```python
drone.flip(direction)
```
#### Direction
Required. The flip direction. Has to be `r` (for right), `l` (for left), `f` (for forward) or `b` (for backward).
### Rotate
```python
drone.rotate(direction, degrees)
```
#### Direction
Required. The rotating direction. Can be  `cw` (for clockwise) or `ccw` (for counterclockwise)
#### Degrees
Required. The number of degrees to rotate. Has to be between 1 and 360.
### MissionPad Registrator (MPR)
```python
drone.MPR()
```
Starts the MissionPad Registrator in a new Thread. This is a Function for registrating MissionPads in both directions (forward and downward). When a MissionPad is found, it will be added to `drone.missionpads` (Dictionary). `drone.missionpads` will look like that:
```python
{
        "1":
            {
                "x-position": 0
                "y-position": 0
                "z-position": 0
            }
        "8":
            {
                "x-position": 5
                "y-position": -3
                "z-position": 12
            }
        }
```
If no MissionPad has been found, this dictionary will be empty. You should be able to send other Commands to the drone while MPR is looking for MissionPads. Every time a new MissionPad has been found, a Text with the ID and the x-, y- and z-position will be printed to the Shell.
### Fly to a MissionPad
```python
drone.goToMP(mid[, speed=100])
```
You have to start MPR to use this Method. If the MissionPad isn't registrated in `drone.missionpads`, a Exception will raise.
#### Mid
Required. The ID of the Mission Pad.
#### Speed
Optional. The speed to fly to thy MissionPad. Default is 100.
