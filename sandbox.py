from lib import tello
import threading
import time

drone = tello()
drone.MPR()
time.sleep(2)
drone.takeoff()
time.sleep(7)
drone.cmd("up 99")
time.sleep(15)
drone.goToMP(1, 100)
