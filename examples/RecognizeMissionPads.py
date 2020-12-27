from lib import tello
import time
import threading
from wireless import Wireless
drone = tello()

drone.cmd("mon")
drone.cmd("mdirection 0")
mid_old = -1
while 1:
    mid = drone.mid()
    if(mid_old != mid):
        print("MissionPad Discovered: " + str(mid))
        print(drone.state())
        mid_old = mid
