from lib import tello
import socket

print("""Tello Library\nCreated by Gabriel Heinzer""")
print("Type a command below")
drone = tello(8890)

while 1:
    command = input(">>>")
    if(command != "read"):
        drone.cmd(command)
