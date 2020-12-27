# tello
This simple Library should help you controlling the TELLO EDU over WiFi with Python

Tested on Windows 10.

## How to import
```python
from tello import tello
drone = tello([port=8890, ip="192.168.10.1"])
```
#### Port
Optional. Sets the port for controlling Tello and reading Data. Default is 8890.
#### IP
Optional. The IP adress for controlling Tello and reading Data. Default is 192.168.10.1.

## Methods
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