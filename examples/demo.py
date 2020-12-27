from lib import tello
import time
import threading
from wireless import Wireless
from console_progressbar import ProgressBar
drone = tello()

steps = 2

def missionPadListener():
    print("Tello is looking for MissionPads with the camera at the Bottom")
    print("#######################")
    print("Actions of the MissionPads:")
    print("")
    print("ID | Aktion")
    print("---+--------------------")
    print("1  | Stop, Right 140 cm")
    print("---+--------------------")
    print("2  | Stop, Left 150 cm")
    print("---+--------------------")
    print("3  | Stop, Land")
    print()
    print("#######################")
    drone.cmd("mon")
    drone.cmd("mdirection 0")
    mid_old = -1
    while 1:
        mid = drone.mid()
        if(mid_old != mid):
            if(mid == 1):
                print("MissionPad Discovered: " + str(mid))
                drone.cmd("stop")
                print("stop")
                time.sleep(3)
                drone.cmd("flip r")
                print("flip r")
                time.sleep(4)
                drone.cmd("land")
                print("land")
            if(mid == 2):
                print("MissionPad Discovered: " + str(mid))
                drone.cmd("stop")
                print("stop")
                time.sleep(3)
                drone.cmd("left 150")
                print("left 150")
            if(mid == 3):
                print("MissionPad Discovered: " + str(mid))
                drone.cmd("stop")
                print("stop")
                time.sleep(3)
                drone.cmd("land")
                print("land")
        mid_old = mid

recvThread = threading.Thread(target=missionPadListener)
recvThread.start()

time.sleep(1)

#print("Battery: " + str(drone.read_battery_level()))
pb = ProgressBar(total=100,prefix='Starting...', suffix='', decimals=3, length=50, fill='#', zfill='-')

pb.print_progress_bar(25)
drone.cmd("speed 55")
#print("speed 11")
time.sleep(2)
pb.print_progress_bar(50)
drone.cmd("takeoff")
#print("takeoff")
time.sleep(15)
pb.print_progress_bar(75)
#drone.cmd("down 33")
#print("down 33")
#time.sleep(7)
drone.cmd("forward 199")
#print("forward 199")
pb.print_progress_bar(100)
drone.cmd(input(">>>"))






