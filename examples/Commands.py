from lib import tello
import socket

print("""Tello Library\nCreated by Gabriel Heinzer""")
print("Type a command below")
drone = tello()

while 1:
    command = input(">>>")
    drone.cmd(command)
