from lib.tello import tello
import socket
drone = tello()

while 1:
    command = input(">>>")
    drone.cmd(command)
